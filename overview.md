What it is
A multi-persona RAG chatbot for a virtual company called Axiom. Instead of one generic AI assistant, you get several department-specialist "personas" — each grounded in that department's real documents, each with a distinct voice, but all sharing the same conversation memory so they stay contextually aware of each other.
The company: Axiom
A fast-moving, first-principles SaaS company (Musk-inspired culture — blunt, data-driven, no fluff, moves fast). You play the CEO.
The personas
PersonaNameHandleKnows aboutVoiceMarketingMarkie@MarkieCampaign reports, brand guidelines, marketing budgetConfident, growth-obsessed, numbers-firstHRPriya@PriyaHiring policy, open roles, leave policyPeople-first but efficient, no bureaucracyFinanceFinn@FinnQuarterly budget, spend approval rulesBlunt, protects runway, ruthless with numbers
How it works (the core mechanic)
You: @Markie should we launch in SEA next month?
→ Markie answers, grounded in Axiom's real marketing docs

You: @Priya do we have people for this?
→ Priya answers — and already knows what Markie just said

You: @Finn can we afford both?
→ Finn answers — aware of the entire conversation so far
One shared knowledge base (Axiom's docs), split by department via metadata filtering. One shared memory across all personas — so switching between them feels like consulting different people in the same meeting, not resetting the conversation.
Why it matters (the real problem)
Removes the "let me check with X department" delay for everyday decisions — cross-functional sanity checks in seconds instead of chasing people across tools/calendars.
Tech stack
LayerChoiceLLMGroqOrchestrationLangChain (Python)Vector DBChroma (local)BackendFastAPIFrontendReactSwitchingExplicit @mentions onlyMemoryShared RunnableWithMessageHistory
What gets built

6 sample docs (2 per persona) simulating Axiom's real internal knowledge
Ingestion pipeline → Chroma vectorstore, tagged by department
3 LangChain RAG chains (one per persona), sharing one conversation history
@mention router to dispatch messages to the right persona
FastAPI backend exposing a /chat endpoint
React frontend — chat window, persona sidebar, per-persona message styling

Build order

Sample docs → 2. Ingestion + Chroma → 3. Persona RAG chains (tested in Python) → 4. FastAPI backend → 5. React frontend