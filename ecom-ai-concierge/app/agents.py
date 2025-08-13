# Lightweight multi-agent orchestration (AutoGen-like) using LangChain chat model as the LLM
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.prompts import PRODUCT_EXPERT_SYSTEM, CUSTOMER_SERVICE_SYSTEM
from app.vector_store import get_chroma_collection
from app import mock_api
from dotenv import load_dotenv
import time

load_dotenv()
from config import LLM_MODEL

class ProductExpertAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)

    def act(self, user_query: str):
        # Search vector DB for supporting documents
        db = get_chroma_collection()
        hits = db.similarity_search(user_query, k=3)
        docs_text = "\n---\n".join([d.page_content for d in hits])

        # Use LLM to create a short structured finding + decide API calls
        prompt = [
            SystemMessage(content=PRODUCT_EXPERT_SYSTEM),
            HumanMessage(content=f"User query: {user_query}\n\nContext docs:\n{docs_text}\n\nAlso check stock for the top product and provide a shipping estimate for postal code 12345 using available APIs.")
        ]
        resp = self.llm(prompt)
        text = getattr(resp, "content", str(resp))

        # For demo we also proactively call the mock API for top product
        top_product_id = hits[0].metadata.get("product_id") if hits else None
        api_info = {}
        if top_product_id:
            stock = mock_api.check_stock(top_product_id)
            shipping = mock_api.get_shipping_estimate(top_product_id, "12345")
            api_info = {"stock": stock, "shipping": shipping, "product_id": top_product_id}

        return {"analysis": text, "api": api_info}

class CustomerServiceAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)

    def act(self, expert_findings: dict, user_query: str):
        prompt = [
            SystemMessage(content=CUSTOMER_SERVICE_SYSTEM),
            HumanMessage(content=f"User query: {user_query}\n\nExpert analysis:\n{expert_findings.get('analysis')}\n\nAPI data:\n{expert_findings.get('api')}")
        ]
        resp = self.llm(prompt)
        return getattr(resp, "content", str(resp))

def run_multi_agent_flow(user_query: str):
    expert = ProductExpertAgent()
    cs = CustomerServiceAgent()

    expert_out = expert.act(user_query)
    # small delay to simulate async handoff
    time.sleep(0.1)
    final = cs.act(expert_out, user_query)
    return {"expert": expert_out, "final": final}

if __name__ == "__main__":
    q = "Find a budget-friendly gaming laptop under $800 that ships fast"
    out = run_multi_agent_flow(q)
    print(out["final"])
