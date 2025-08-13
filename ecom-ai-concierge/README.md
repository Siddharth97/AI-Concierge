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

# AI-Concierge
activate the venv
``
python3.12 -m venv .venv
source .venv/bin/activate
pip install numpy==1.26.4 pandas==2.2.1
``

For dependency resolution
``
pip install -r requirements.txt --use-feature=fast-deps
``

To get all requirements in requirements.txt
''
pip freeze > requirements.txt
``

Downgrade python to 3.12 latest package does not have support for packages
``
brew install python-gdbm@3.12
``

OPENAI_API_KEY=<OPEN_API_KEY>
#populate the db after activating venv
``
python app/populate_and_test_vectorstore.py 
``
#run the app

``
streamlit run streamlit_app.py  
``

Sample Prompts

Here are some example prompts you can try with the AI-Concierge:

	•	I’m looking for a stylish purse suitable for both office and casual outings, preferably with multiple compartments. Also, what is your international shipping policy and typical delivery times?
	•	Compare the features and prices of the Tory Burch Robinson Tote and the Perry Triple-Compartment Tote. Additionally, if I receive a damaged item, what steps should I follow according to your return policy?
	•	I want a compact wallet with multiple card slots and a chain strap option for versatility. Could you also explain the warranty duration and coverage on these products?
