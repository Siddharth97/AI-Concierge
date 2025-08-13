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


2️⃣ Create .env with your OpenAI API key
bash```
echo "OPENAI_API_KEY=sk-..." > .env


3️⃣ Create Python venv and install dependencies
bash```
python3.12 -m venv .venv
source .venv/bin/activate
pip install numpy==1.26.4 pandas==2.2.1
pip install -r requirements.txt --use-feature=fast-deps
```

4️⃣ (Optional) Save your current dependencies
bash```
pip freeze > requirements.txt
```

5️⃣ Populate the database
bash```
python app/populate_and_test_vectorstore.py
```

6️⃣ Run the Streamlit app
bash```
streamlit run streamlit_app.py
```

Python Version Notes

Some dependencies may not support Python 3.13 yet.
To downgrade to Python 3.12 on macOS with Homebrew:

bash```
brew install python-gdbm@3.12
```

Project Notes
	•	This scaffold uses mock API endpoints in app/mock_api.py. Replace these with real commerce APIs if needed.
	•	Chroma vector store persists locally in ./chroma_db.
	•	LangChain agents use tool-based calling to simulate function-call behavior.

   Sample Prompts

Here are some example prompts you can try with the AI Concierge:
	•	I’m looking for a stylish purse suitable for both office and casual outings, preferably with multiple compartments. Also, what is your international shipping policy and typical delivery times?
	•	Compare the features and prices of the Tory Burch Robinson Tote and the Perry Triple-Compartment Tote. Additionally, if I receive a damaged item, what steps should I follow according to your return policy?
	•	I want a compact wallet with multiple card slots and a chain strap option for versatility. Could you also explain the warranty duration and coverage on these products?
