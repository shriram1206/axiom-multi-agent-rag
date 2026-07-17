ravan/
├── Sample_data/
│   ├── marketing_budget.md      (Maya's docs)
│   ├── q3_campaign_report.md    
│   ├── hiring_policy.md         (Vibhishana's docs)
│   ├── open_roles.md
│   ├── q3_budget.md             (Kubera's docs)
│   └── spend_approval_policy.md
├── backend/
│   ├── main.py           # FastAPI app (handles /chat, @mentions, RAG, and memory)
│   ├── personas.py       # Persona configs (Maya, Vibhishana, Kubera)
│   ├── ingest.py         # Doc loader & chunking script
│   ├── chroma_db/        # Local vector database (auto-generated)
│   ├── .env              # GROQ_API_KEY
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Landing Page & Dashboard toggler
│   │   ├── App.css               # Layout styling
│   │   ├── index.css             # Global minimalist styling & typography
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx    # Main chat interface
│   │   │   ├── MessageBubble.jsx # Styled per-persona messages
│   │   │   └── PersonaSidebar.jsx# Shows active personas, click to @mention
│   │   └── api.js                # Helper to call FastAPI backend
│   ├── package.json
│   └── vite.config.js
├── overview.md
└── tech_stack.md