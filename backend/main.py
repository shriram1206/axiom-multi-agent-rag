from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import re
import asyncio

from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from personas import PERSONAS

load_dotenv()

app = FastAPI(title="Axiom Multi-Persona RAG (Production Grade)")

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Graceful DB Loading
DB_DIR = "./chroma_db"
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

if os.path.exists(DB_DIR):
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embedding_function)
    print("Successfully loaded Chroma vector store.")
else:
    print("Warning: Chroma DB not found. Run ingest.py first.")
    vectorstore = None

# We use a fast, capable open-source model via Groq
llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant")

# 2. Session-based Memory Management (replaces global state)
active_sessions = {}

class ChatRequest(BaseModel):
    session_id: str = "default_session"
    message: str

def parse_mention(message: str):
    # Extracts the first @Name from the message
    match = re.search(r'@(\w+)', message)
    if match:
        name = match.group(1).lower()
        if name in PERSONAS or name in ["all", "status"]:
            return name
    return None

async def fetch_agent_response(p_name: str, user_msg: str, mode: str):
    """Helper function to fetch a specific response from a single persona asynchronously."""
    p_config = PERSONAS[p_name]
    p_dept = p_config["department"]
    
    try:
        retriever = vectorstore.as_retriever(search_kwargs={'filter': {'department': p_dept}, 'k': 2})
        docs = await retriever.ainvoke(user_msg)
        context = "\n\n".join([doc.page_content for doc in docs])
    except Exception:
        context = "No context available."
        
    if mode == "status":
        prompt_instruction = "The CEO is asking for a general status update on the company. Provide a 2-3 sentence summary of your department's current priorities, budget, or blockers based ONLY on the context."
    else: # mode == "all"
        prompt_instruction = "The CEO has issued a company-wide directive. Based on your specific departmental data, respond with how this impacts you. Frame your response strictly as: 'Currently we have [exact data from context], to execute this we will need [new requirement/constraint].' Keep it under 3 sentences, extremely blunt, data-driven, and no-fluff."
        
    prompt = f"{p_config['system_prompt']}\n\nContext:\n{context}\n\n{prompt_instruction} Do not prefix your name."
    
    messages = [SystemMessage(content=prompt), HumanMessage(content=user_msg)]
    resp = await llm.ainvoke(messages)
    
    title = "Marketing" if p_name == "maya" else "HR" if p_name == "vibhishana" else "Finance"
    return f"**{p_name.capitalize()} ({title})**:\n{resp.content}\n"

@app.post("/chat")
async def chat(request: ChatRequest):
    if not vectorstore:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Vector database is offline. Please run ingest.py."
        )

    user_msg = request.message
    session_id = request.session_id
    
    # 1. Parse which persona is mentioned
    persona_name = parse_mention(user_msg)
    if not persona_name:
        return {"response": "Error: You must mention a valid persona (e.g., @Maya, @Vibhishana, @Kubera, @all, or @status).", "persona": "System"}
    
    # Initialize session memory if it doesn't exist
    if session_id not in active_sessions:
        active_sessions[session_id] = []
    
    session_history = active_sessions[session_id]

    # --- SPECIAL ROUTE: @status and @all ---
    # Trigger multi-agent parallel generation
    if persona_name in ["status", "all"]:
        tasks = [
            fetch_agent_response("maya", user_msg, persona_name),
            fetch_agent_response("vibhishana", user_msg, persona_name),
            fetch_agent_response("kubera", user_msg, persona_name)
        ]
        
        # Run all 3 LLM calls in parallel for speed!
        results = await asyncio.gather(*tasks)
        combined_response = "\n".join(results)
        
        session_history.append({"role": "user", "content": user_msg})
        session_history.append({"role": "assistant", "content": combined_response})
        
        return {"response": combined_response, "persona": "Executive Team"}

    # --- STANDARD ROUTE ---
    persona_config = PERSONAS[persona_name]
    department = persona_config["department"]
    
    # 2. Retrieve relevant context from Chroma asynchronously
    if department == "all":
        retriever = vectorstore.as_retriever(
            search_kwargs={'k': 4} # Broad search for the whole team
        )
    else:
        retriever = vectorstore.as_retriever(
            search_kwargs={'filter': {'department': department}, 'k': 3}
        )
    
    try:
        docs = await retriever.ainvoke(user_msg)
        context = "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        docs = retriever.invoke(user_msg)
        context = "\n\n".join([doc.page_content for doc in docs])

    # 3. Construct the prompt manually
    system_prompt = persona_config["system_prompt"]
    
    augmented_system_message = f"""{system_prompt}
    
    You have access to the following internal company documents (Context):
    {context}
    
    Read the conversation history to understand the context of the meeting so far.
    """

    messages = [SystemMessage(content=augmented_system_message)]
    
    # Add shared history for this specific session
    for msg in session_history[-10:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
            
    # Add the current user message
    messages.append(HumanMessage(content=user_msg))

    # 4. Generate Response Asynchronously
    try:
        response = await llm.ainvoke(messages)
        ai_text = response.content
        
        # Save to session-specific memory
        session_history.append({"role": "user", "content": user_msg})
        session_history.append({"role": "assistant", "content": f"({persona_name.capitalize()}): {ai_text}"})
        
        return {"response": ai_text, "persona": persona_name.capitalize()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Generation Error: {str(e)}")

class ResetRequest(BaseModel):
    session_id: str = "default_session"

@app.post("/reset")
async def reset_memory(request: ResetRequest):
    if request.session_id in active_sessions:
        active_sessions[request.session_id] = []
    return {"status": f"Memory cleared for session {request.session_id}"}
