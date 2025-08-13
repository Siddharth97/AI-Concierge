from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

PERSIST_DIR = "./chroma_db"

def main():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    docs = [
        Document(page_content="Apples are red and sweet.", metadata={"source": "fruit_facts"}),
        Document(page_content="Bananas are yellow and soft.", metadata={"source": "fruit_facts"})
    ]

    print("Adding documents...")
    vectordb.add_documents(docs)

    query = "Which fruit is yellow?"
    results = vectordb.similarity_search(query, k=2)

    print("\nQuery:", query)
    for r in results:
        print("-", r.page_content, "| metadata:", r.metadata)

if __name__ == "__main__":
    main()