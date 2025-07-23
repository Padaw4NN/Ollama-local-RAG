import sys
import asyncio
import streamlit as st
from src import run_chain, insert_all


if "--retrieve-data" in sys.argv:
    insert_all()
    print("\n✅ The data has been inserted!")
    print("🚀 Now you can run: $ streamlit run main.py\n")
    exit(0)


st.title("Pizza review RAG")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Enter your query:")

if st.button("Send") and query:
    with st.spinner("Generating response..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(run_chain(query))
    st.session_state.history.append({"user": query, "assistant": response})
