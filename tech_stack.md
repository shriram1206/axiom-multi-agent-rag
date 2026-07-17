## Ravan — Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | Groq | Powers each persona's reasoning/responses |
| **Orchestration** | LangChain (Python) | RAG chains, routing, shared memory |
| **Vector Database** | Chroma (local) | Stores embedded Axiom docs, filtered by department |
| **Backend** | FastAPI | Exposes `/chat` endpoint, runs persona logic |
| **Frontend** | React | Chat UI, persona sidebar, message styling |
| **Persona Routing** | Custom `@mention` parser | Dispatches messages to correct persona |
| **Memory** | LangChain `RunnableWithMessageHistory` (in-memory) | Shared conversation context across all personas |
| **Document Storage** | Local `.md` files (`data/` folder) | Source docs per department, loaded at ingestion |
| **Language** | Python (backend) + JavaScript/JSX (frontend) | Core implementation languages |