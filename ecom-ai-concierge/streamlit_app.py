import streamlit as st
from dotenv import load_dotenv
from app.vector_store import init_vectorstore, get_chroma_collection
from app import chains
from app import agents
from app.prompts import SYSTEM_PROMPT
import os
import pandas as pd
from config import USE_AUTOGEN

load_dotenv()

st.set_page_config(layout="wide")

# Initialize vector store on first run
with st.spinner("Initializing vector store..."):
    db = init_vectorstore()

# UI layout
st.title("Tory Burch AI Concierge — Hackathon POC")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Chat")
    if "history" not in st.session_state:
        st.session_state.history = []

    query = st.text_input("Ask about products, orders, or policies:")
    if st.button("Send") and query:
        st.session_state.history.append({"role": "user", "text": query})

        if USE_AUTOGEN:
            out = agents.run_multi_agent_flow(query)
            # show internals
            st.session_state.history.append({"role": "product_expert", "text": out["expert"]["analysis"]})
            st.session_state.history.append({"role": "assistant", "text": out["final"]})
        else:
            try:
                # Use retrieval-augmented QA chain here instead of just the tool-enabled agent
                response = chains.run_qa_chain(query)
                answer = response.get("result") if isinstance(response, dict) else response
            except Exception as e:
                answer = f"QA chain error: {e}"
            st.session_state.history.append({"role": "assistant", "text": answer})

    for msg in st.session_state.history[::-1]:
        role = msg["role"]
        if role == "user":
            st.markdown(f"**User:** {msg['text']}")
        elif role == "assistant":
            st.markdown(f"**Assistant:** {msg['text']}")
        elif role == "product_expert":
            st.markdown(f"<div style='background:#E8F0FE;padding:8px;border-radius:6px'><b>Product Expert (internal):</b><br/>{msg['text']}</div>", unsafe_allow_html=True)

with col2:
    st.subheader("Agent Conversation Log")
    st.write("System prompt:")
    st.code(SYSTEM_PROMPT)
    # st.write("Example queries:")
    # if st.button("Find me all wallets under $500"):
    #     st.session_state.history = []
    #     st.session_state.history.append({"role": "user", "text": "Find a budget gaming laptop under $800 that ships fast."})
    #     st.experimental_rerun()

    # st.write("Vector DB stats:")
    # try:
    #     df = pd.read_csv("data/products.csv")
    #     st.write(f"Products in catalog: {len(df)}")
    # except Exception:
    #     st.write("Vector DB introspection unavailable.")