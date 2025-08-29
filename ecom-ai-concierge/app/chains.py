import csv
import sys
from dotenv import load_dotenv
from config import LLM_MODEL
from app.vector_store import get_retriever

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.evaluation import EmbeddingDistanceEvalChain

load_dotenv()

# ---------------------------------------------------
# TOOL for function calling
# ---------------------------------------------------
@tool
def search_products(query: str) -> str:
    """Searches the product database and returns matching results."""
    return run_qa_chain(query)

# ---------------------------------------------------
# QA Chain
# ---------------------------------------------------
def run_qa_chain(query: str):
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)
    retriever = get_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa_chain.invoke({"query": query})
    return result["result"] if isinstance(result, dict) else result

# ---------------------------------------------------
# Agent using OpenAI function calling
# ---------------------------------------------------
def run_agent(query: str):
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    tools = [search_products]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )
    return agent.run(query)

# ---------------------------------------------------
# Batch Semantic Evaluation
# ---------------------------------------------------
def batch_evaluate(file_path: str):
    embeddings = OpenAIEmbeddings()
    eval_chain = EmbeddingDistanceEvalChain(embedding=embeddings, distance_metric="cosine")

    examples = []
    predictions = []

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            query = row["query"]
            ideal_answer = row["ideal_answer"]

            prediction = run_qa_chain(query)

            examples.append({"query": query, "ideal": ideal_answer})
            predictions.append({"result": prediction})

            print(f"Query: {query}")
            print(f"Predicted: {prediction}")
            print(f"Ideal: {ideal_answer}\n")

    print("\n--- Semantic Evaluation Results ---")
    for i, ex in enumerate(examples):
        eval_result = eval_chain.evaluate_strings(
            prediction=predictions[i]["result"],
            reference=ex["ideal"]
        )
        similarity = 1 - eval_result["score"]
        color = "\033[92m" if similarity >= 0.85 else "\033[91m"
        reset = "\033[0m"

        print(f"Q{i+1}: {ex['query']}")
        print(f"Semantic Similarity: {color}{similarity:.2f}{reset}")
        print("-------------------------")

# ---------------------------------------------------
# CLI Entry
# ---------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 1:
        batch_evaluate("data/eval_dataset.csv")
    elif sys.argv[1] == "agent":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Find a budget purse under $800"
        print(run_agent(query))
    elif sys.argv[1] == "qa":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Find a budget purse under $800"
        print(run_qa_chain(query))