import streamlit as st
import time
import os
from dotenv import load_dotenv

from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS


# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
# Make NVIDIA API key available to the NVIDIA SDK
os.environ["NVIDIA_API_KEY"] = os.getenv("NVIDIA_API_KEY", "")

# Ensure required session-state keys exist (avoid AttributeError on first run)
for key in ("embeddings", "loader", "docs", "text_splitter", "final_documents", "vectors"):
    st.session_state.setdefault(key, None)

# Initialize the NVIDIA LLM (Meta Llama 3 70B Instruct)
llm = ChatNVIDIA(model="meta/llama3-70b-instruct")


# ------------------------------------------------------------
# Build vector index (load PDFs -> split -> embed -> FAISS)
# ------------------------------------------------------------
def vector_embedding():
    """
    Loads PDFs from ./pdfs, splits them into chunks, generates embeddings
    with NVIDIAEmbeddings, and stores them in a FAISS vector index
    kept in Streamlit session_state.
    """
    # Only (re)build if we don't already have a vector index
    if st.session_state.get("vectors") is None:
        # 1) Embeddings model (NVIDIA API)
        st.session_state.embeddings = NVIDIAEmbeddings()

        # 2) Load PDFs from local folder
        st.session_state.loader = PyPDFDirectoryLoader("./pdfs")
        st.session_state.docs = st.session_state.loader.load()

        if not st.session_state.docs:
            st.warning("No PDFs found in ./pdfs. Please add some files.")
            return

        # 3) Split text into overlapping chunks to fit embedding model limits
        #    (400 chars per chunk, 50 chars overlap to preserve context)
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50,
        )

        # 4) (Demo) Limit number of documents processed to speed up prototypes
        split_docs = st.session_state.text_splitter.split_documents(
            st.session_state.docs[:10]
        )
        st.session_state.final_documents = split_docs

        # 5) Create FAISS vector store from document chunks + embeddings
        st.session_state.vectors = FAISS.from_documents(
            st.session_state.final_documents,
            st.session_state.embeddings,
        )


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("PDF Question Answering with NVIDIA Embeddings and LLMs")

# Prompt template: instruct the LLM to answer strictly from provided context
prompt = ChatPromptTemplate.from_template(
    """
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question.

<context>
{context}
</context>
Question: {input}
"""
)

# Button to build the vector index explicitly
if st.button("Document Embedding", key="embed_btn"):
    vector_embedding()
    if st.session_state.get("vectors") is not None:
        st.success("FAISS Vector Store DB is ready using NVIDIA Embeddings")

# User input: natural-language question about the PDFs
user_q = st.text_input("Enter your question from documents")

response = None  # will hold the retrieval+generation result


# ------------------------------------------------------------
# Run retrieval-augmented generation when user submits a question
# ------------------------------------------------------------
if user_q:
    # Auto-build the index if user asked a question before clicking the button
    if st.session_state.get("vectors") is None:
        vector_embedding()

    # Proceed only if we actually have a vector index
    if st.session_state.get("vectors") is not None:
        # Chain that stuffs retrieved docs into the prompt for the LLM
        document_chain = create_stuff_documents_chain(llm, prompt)

        # Convert FAISS index to a retriever (kNN search over embeddings)
        retriever = st.session_state.vectors.as_retriever()

        # Retrieval chain = retriever + document_chain (LLM)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        # Measure end-to-end response time
        t0 = time.perf_counter()
        response = retrieval_chain.invoke({"input": user_q})
        st.caption(f"Response time: {time.perf_counter() - t0:.2f}s")

        # Different LC versions may return 'answer' or 'output_text'
        st.write(response.get("answer") or response.get("output_text") or response)
    else:
        st.warning("Please add PDFs to ./pdfs and build the vector index first.")


# ------------------------------------------------------------
# Transparency: show the retrieved chunks used as context
# ------------------------------------------------------------
if response and "context" in response:
    with st.expander("Document Similarity Search"):
        # Display each retrieved chunk and a separator
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("-----------------------------")
else:
    st.info("Run a query to see document similarity results.")
