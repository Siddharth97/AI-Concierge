import os
import shutil
import pandas as pd
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Load environment variables from .env
load_dotenv()

# Change this to your vector store directory
PERSIST_DIR = "./chroma_db"

# Your product CSV path
PRODUCTS_CSV = "data/products.csv"
FAQS_PATH = "data/faqs.txt"  # optional


def load_products_csv(path=PRODUCTS_CSV):
    df = pd.read_csv(path)
    docs = []
    for _, row in df.iterrows():
        content = (
            f"Name: {row['name']}\nCategory: {row['category']}\n"
            f"Price: {row['price']}\nDescription: {row['description']}"
        )
        meta = {
            "product_id": row["product_id"],
            "name": row["name"],
            "price": row["price"],
        }
        docs.append(Document(page_content=content, metadata=meta))
    return docs


def load_faqs(path=FAQS_PATH):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [Document(page_content=text, metadata={"source": "faqs"})]


def main():
    # Make sure API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not set. Please add it to your .env file in the project root."
        )

    # Delete existing vector store dir to start fresh
    if os.path.exists(PERSIST_DIR):
        print(f"Removing existing vector store at {PERSIST_DIR}")
        shutil.rmtree(PERSIST_DIR)

    print("Loading documents...")
    product_docs = load_products_csv()
    faq_docs = load_faqs()
    all_docs = product_docs + faq_docs
    print(f"Loaded {len(all_docs)} documents total.")

    # Initialize embeddings & vector store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
    vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

    print("Adding documents to vector store...")
    vectordb.add_documents(all_docs)

    # Test retrieval
    query = "Find a budget gaming laptop under $800"
    print(f"\nTesting retrieval for query: '{query}'")
    results = vectordb.similarity_search(query, k=4)

    if not results:
        print("No documents found!")
    else:
        for i, doc in enumerate(results, 1):
            print(f"Doc {i} preview:\n{doc.page_content[:200]}...\n")


if __name__ == "__main__":
    main()