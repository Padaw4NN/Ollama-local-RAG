import streamlit as st

from src.vector_store import (
    client,
    embeddings,
    QDRANT_COLLECTION
)

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate


PROMPT = """
You are an expert in analyzing pizzeria reviews.
You answers only about the context that will be provided to you.
If the query is not about the context, just answer `I can't answer that`.

context:
{context}

query:
{query}
"""

llm_model = OllamaLLM(model="llama3.2")
llm_template = PromptTemplate.from_template(PROMPT)

llm_chain = llm_template | llm_model

async def run_chain(query: str) -> str:
    """
    """
    input_vector = await embeddings.aembed_query(text=query)

    result_query = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=input_vector,
        with_payload=True,
        limit=2
    )

    context = "\n\n".join([point.payload["text"] for point in result_query.points])

    placeholder = st.empty()
    response = ""
    async for chunk in llm_chain.astream({"context": context, "query": query}):
        response += chunk
        placeholder.markdown(response)

    return response
