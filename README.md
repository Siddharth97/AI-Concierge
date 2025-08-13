# AI-Concierge
activate the venv
``
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
``

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