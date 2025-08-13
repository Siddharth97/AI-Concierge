import os
import shutil
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
from config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL

def load_products_csv(path="data/products.csv"):
    import pandas as pd
    df = pd.read_csv(path)
    docs = []
    for _, row in df.iterrows():
        content = (
            f"Name: {row['name']}\nCategory: {row['category']}\n"
            f"Price: {row['price']}\nDescription: {row['description']}"
        )
        meta = {"product_id": row['product_id'], "name": row['name'], "price": row['price']}
        docs.append(Document(page_content=content, metadata=meta))
    return docs

def load_faqs(path="data/faqs.txt"):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [Document(page_content=text, metadata={"source": "faqs"})]

def is_persist_dir_populated(persist_directory=CHROMA_PERSIST_DIR):
    # Check if directory exists and has at least one file/dir inside
    if not os.path.exists(persist_directory):
        return False
    return any(os.scandir(persist_directory))

def get_chroma_collection(persist_directory=CHROMA_PERSIST_DIR, embedding_model=EMBEDDING_MODEL):
    embeddings = OpenAIEmbeddings(model=embedding_model)
    if is_persist_dir_populated(persist_directory):
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    else:
        vectordb = Chroma.from_documents([], embedding=embeddings, persist_directory=persist_directory)
    return vectordb

def init_vectorstore(persist_directory=CHROMA_PERSIST_DIR):
    vectordb = get_chroma_collection(persist_directory)
    if not is_persist_dir_populated(persist_directory):
        docs = load_products_csv() + load_faqs()
        print(f"Loaded {len(docs)} documents from CSV and FAQ")
        if len(docs) == 0:
            print("Warning: No documents loaded to populate the vector store!")
        else:
            vectordb.add_documents(docs)
            vectordb.persist()
            print("Vector store populated and persisted.")
    else:
        print("Vector store already populated.")
    return vectordb

def get_retriever(persist_directory=CHROMA_PERSIST_DIR):
    vectordb = get_chroma_collection(persist_directory)
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    return retriever

if __name__ == "__main__":
    db = init_vectorstore()
    print("Vector store initialized.")