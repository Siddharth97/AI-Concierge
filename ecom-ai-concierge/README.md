E-commerce AI Concierge (Hackathon Scaffold)

Overview

This is a proof-of-concept e-commerce conversational assistant demonstrating:
	•	Vector DB retrieval (Chroma + OpenAI embeddings)
	•	LangChain chains and tool-based function calling (mock APIs)
	•	Optional AutoGen-like multi-agent orchestration mode
	•	Streamlit chat UI showing agent role conversations

Default mode: LangChain single-agent.
Toggle AutoGen mode in config.py.

⸻

Quickstart

1️⃣ Clone or download the repo
bash```
git clone <your-repo-url>
cd ecom-ai-concierge
```

bash```
echo "OPENAI_API_KEY=sk-..." > .env
```

bash```
python3.12 -m venv .venv
source .venv/bin/activate
pip install numpy==1.26.4 pandas==2.2.1
pip install -r requirements.txt --use-feature=fast-deps
```

bash```
pip freeze > requirements.txt
```

bash```
python app/populate_and_test_vectorstore.py
```

bash```
streamlit run streamlit_app.py
```