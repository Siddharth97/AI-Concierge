# E-commerce AI Concierge (Hackathon Scaffold)

## Overview
This is a proof-of-concept e-commerce conversational assistant demonstrating:
- Vector DB retrieval (Chroma + OpenAI embeddings)
- LangChain chains and tool-based function calling (mock APIs)
- Optional AutoGen-like multi-agent orchestration mode
- Streamlit chat UI showing agent role conversations

Default mode: LangChain single-agent. Toggle AutoGen mode in `config.py`.

## Quickstart
1. Copy repo locally (or download the zip provided by this project).
2. Create `.env` with your OpenAI API key:
   ```bash
   echo "OPENAI_API_KEY=sk-..." > .env
   ```
3. Create Python venv and install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Notes
- This scaffold uses **mock API** endpoints in `app/mock_api.py`. Replace with real commerce APIs if you want.
- Chroma vector store persists locally inside `./chroma_db` by default.
- LangChain agents use tool-based calling to show function-call-like behavior.

Enjoy — replace the sample data in `data/` with your company dataset for the hackathon.
