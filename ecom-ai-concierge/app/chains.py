from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from app.vector_store import get_retriever
from dotenv import load_dotenv
load_dotenv()
from config import LLM_MODEL

def test_search():
    retriever = get_retriever()
    results = retriever.similarity_search("budget a wallet", k=3)
    print(f"Search results count: {len(results)}")
    for r in results:
        print(r.page_content)

def run_qa_chain(query: str):
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)
    retriever = get_retriever()

    # DEBUG: print retrieved docs before running QA chain
    docs = retriever.get_relevant_documents(query)  # deprecated but useful for debug
    print(f"Retrieved {len(docs)} documents for query: '{query}'")
    for i, doc in enumerate(docs):
        print(f"Doc {i+1} preview: {doc.page_content[:300]}")

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa_chain.invoke({"query": query})  # or use qa_chain.run(query)
    return result

if __name__ == "__main__":
    test_search()
    question = "Find a budget purse under $800"
    answer = run_qa_chain(question)
    print(f"QA chain answer: {answer}")