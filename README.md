# Axiom Multi-Agent RAG 🚀

A production-grade, multi-agent Retrieval-Augmented Generation (RAG) dashboard. Axiom OS simulates a corporate C-suite where distinct AI personas (Marketing, HR, Finance) collaborate, enforce strict company policies, and retrieve highly specific data from isolated knowledge bases.

## ✨ Core Architecture

Instead of a single "know-it-all" chatbot, this system utilizes **Multi-Agent Orchestration**.

*   **Maya (Marketing Lead)**: Only accesses marketing budgets and campaign data.
*   **Vibhishana (People Lead)**: Strictly enforces hiring policies and notice periods.
*   **Kubera (Finance Lead)**: Aggressively protects the runway and vetoes unapproved budgets.

When interacting with the dashboard, the agents maintain a **shared conversation history**, allowing them to "hear" what other executives are approving or rejecting, enabling true cross-functional AI reasoning.

## ⚡ Key Features

*   **Parallel Multi-Agent Routing**: Using the `@status` or `@all` command triggers an `asyncio.gather` pipeline. The backend fires simultaneous, independent RAG queries to all three agents, stitching together a unified boardroom response in under 2 seconds.
*   **Strict Data Isolation**: Vector searches are heavily filtered by department metadata (`search_kwargs={'filter': {'department': department}}`). The HR agent physically cannot retrieve or leak confidential Marketing data.
*   **Session-Based Memory**: The FastAPI backend isolates conversation history by `session_id`, meaning 50 different users could hit the endpoints simultaneously without memory contamination.
*   **Zero Action Hallucination**: Extensive prompt engineering guarantees the executives act as *advisors*. They actively push back on impossible requests and never hallucinate taking physical system actions.

## 🛠 Tech Stack

*   **LLM Engine**: Groq (`llama-3.1-8b-instant`) for sub-second inference.
*   **Orchestration**: LangChain (Python) & `asyncio`.
*   **Vector Database**: ChromaDB (Local SQLite/Parquet).
*   **Backend**: FastAPI (Async endpoints).
*   **Frontend**: React & Vite (Custom minimalist CSS, no Tailwind).

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/shriram1206/axiom-multi-agent-rag.git
cd axiom-multi-agent-rag
```

### 2. Start the FastAPI Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

# Create your environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run the ingestion script to build the local Chroma DB
python ingest.py

# Start the server
uvicorn main:app --reload
```

### 3. Start the React Frontend
```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

## 🎯 Usage (The Dashboard)

Once both servers are running, open the React frontend and click **"Deploy Axiom"**. 

In the chat interface, use the following routing commands:
*   `@Maya what is our remaining Q3 budget?`
*   `@Vibhishana I want to hire 4 new engineers immediately.` *(Watch her reject this based on strict RAG policy).*
*   `@Kubera did you see what Vibhishana just said?` *(Tests shared agent memory).*
*   `@status give me a company update.` *(Triggers the parallel multi-agent summary).*
*   `@all we are going to double our headcount next month.` *(Forces all agents to evaluate the constraint simultaneously).*
