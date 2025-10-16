# backend.py
import streamlit as st
from dotenv import load_dotenv
import os
import time

# 1. Import necessary libraries

from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
# from langchain.agents import Tool, initialize_agent

# for memory in the chat
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain


# # ---------------------------
# # Configure your API keys (with 'sectrets')
# # ---------------------------
def setup_environment():
    """
    Get API keys from Streamlit secrets or environment variables
    """
    # First try environment variables (works everywhere)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

    # Try Streamlit secrets first
    if hasattr(st, 'secrets') and st.secrets:
        if "OPENAI_API_KEY" in st.secrets and "PINECONE_API_KEY" in st.secrets:
            OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
            PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
            index_name = "gdpr-compliance-openai"
            return index_name, OPENAI_API_KEY, PINECONE_API_KEY
    
    # Fallback to environment variables
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    index_name = "gdpr-compliance-openai"
    
    if OPENAI_API_KEY and PINECONE_API_KEY:
        return index_name, OPENAI_API_KEY, PINECONE_API_KEY
    else:
        print("❌ API keys not found in secrets or environment variables")
        return None, None, None

# Initialize environment
index_name, OPENAI_API_KEY, PINECONE_API_KEY = setup_environment()

# ========== ADD LANGSMITH SETUP RIGHT HERE ==========
def setup_langsmith():
    """
    Setup LangSmith tracing for observability
    """
    # Try Streamlit secrets first
    if hasattr(st, 'secrets') and st.secrets:
        if "LANGSMITH_API_KEY" in st.secrets:
            # Set the EXACT environment variables LangSmith expects
            os.environ["LANGSMITH_TRACING"] = st.secrets.get("LANGSMITH_TRACING", "true")
            os.environ["LANGSMITH_API_KEY"] = st.secrets["LANGSMITH_API_KEY"]
            # os.environ["LANGSMITH_ENDPOINT"] = st.secrets.get("LANGSMITH_ENDPOINT", "https://eu.api.smith.langchain.com")
            os.environ["LANGSMITH_PROJECT"] = st.secrets.get("LANGSMITH_PROJECT", "GDPR-Compliance-Assistant")
            
            print("✅ LangSmith tracing configured!")
            print(f"   Project: {os.environ['LANGSMITH_PROJECT']}")
            return True
    else:
        print("⚠️  LangSmith API key not found - tracing disabled")
        return False

    # # Fallback to environment variables
    # LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    # if LANGSMITH_API_KEY:
    #     LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "GDPR-Compliance-Assistant")
    #     os.environ["LANGCHAIN_TRACING_V2"] = "true"
    #     os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
    #     os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
    #     return True
    # else:
    #     print("⚠️  LangSmith API key not found - tracing disabled")
    #     return False

# Initialize LangSmith
langsmith_enabled = setup_langsmith()
# ========== END OF LANGSMITH SETUP ==========

# ---------------------------
# Pinecone Initialization
# ---------------------------
def init_pinecone(api_key: str, index_name: str = "gdpr-compliance-openai", environment: str = "us-east-1"):
    """
    Initialize Pinecone connection using current Pinecone
    """
    if not api_key:
        raise ValueError("PINECONE_API_KEY is missing!")
    
    # Initialize Pinecone
    pc = Pinecone(api_key=api_key)
    
    # Check if index exists
    if index_name in pc.list_indexes().names():
        # Wait for index to be ready
        while not pc.describe_index(index_name).status.ready:
            time.sleep(1)
    else:
        print(f"⚠️  Index '{index_name}' not found.")
    
    # Get the index object
    index = pc.Index(index_name)
    return pc, index

# ---------------------------
# Embeddings Initialization 
# ---------------------------
def init_embeddings():
    """
    Initialize OpenAI embeddings
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing!")
    
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_API_KEY
    )
    return embeddings

# ---------------------------
# vector store connection Initialization 
# ---------------------------
def init_vector_store():
    """
    Initialize the vector store connection
    """
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is missing!")
    
    pc, index = init_pinecone(PINECONE_API_KEY)
    embeddings = init_embeddings()
    
    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        text_key="text"
    )
    return vector_store

# ---------------------------
# LLM Initialization 
# ---------------------------
def init_llm():
    """
    Initialize the LLM
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing!")
        
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name='gpt-3.5-turbo',
        temperature=0.0,
        max_tokens=500,
    )
    return llm

# ---------------------------
# QA Chain Initialization 
# ---------------------------
def create_qa_chain():
    """
    Create the QA chain with English prompt
    """
    
    vector_store = init_vector_store()
    llm = init_llm()
    
    # Create retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    # English prompt template
    prompt_template_en = """You are a privacy assistant specialized in GDPR, 'AI & Data Protection' for small german businesses. 
Explain in a clear, practical, and easy-to-understand way based on the following context. 
This is not legal advice. If the context does not contain the answer, say so openly.

Context:
{context}

Question:
{question}

Answer (short and practical):"""

    PROMPT_en = PromptTemplate(
        template=prompt_template_en, 
        input_variables=["context", "question"]
    )
    
    # Create QA chain
    qa_chain_en = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT_en},
        return_source_documents=True
    )
    
    return qa_chain_en

# ---------------------------
# QA Memory (opt.)  Initialization 
# ---------------------------

def create_qa_chain_with_memory():
    """Create QA chain with conversation memory"""
    
    vector_store = init_vector_store()
    llm = init_llm()
    
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    memory = ConversationBufferWindowMemory(
        k=3,  # Remember last 3 exchanges
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    # Custom prompt template for memory-based conversations
    prompt_template_mem = """You are a privacy assistant specialized in GDPR for small craft businesses.
Use the following context and conversation history to answer the question. 
Explain in a clear, practical way. This is not legal advice. If the context does not contain the answer, say so openly.

Previous conversation:
{chat_history}

Context:
{context}

Human:
{question}

Answer (short and practical):"""

    PROMPT_mem = PromptTemplate(
        template=prompt_template_mem,
        input_variables=["chat_history", "context", "question"]
    )
    
    # ✅ Use ConversationalRetrievalChain with custom prompt
    qa_chain_mem = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT_mem},
        return_source_documents=True,
        verbose=False  # Set to True to see the chain thinking
    )
    
    return qa_chain_mem, memory

# ---------------------------
#  Ask a question WITH MEMORY and return answer
# ---------------------------

def ask_gdpr_question_with_memory(question, show_sources=True):
    """
    Ask a question with conversation memory and return answer with sources
    """
    global qa_chain_memory, memory_instance
    
    # Check if API keys are available
    if not OPENAI_API_KEY or not PINECONE_API_KEY:
        return {
            "answer": "❌ API keys not configured. Please set OPENAI_API_KEY and PINECONE_API_KEY in Streamlit secrets.",
            "sources": [],
            "memory_count": 0
        }
    
    # Initialize chain and memory if not already done
    if qa_chain_memory is None or memory_instance is None:
        qa_chain_memory, memory_instance = create_qa_chain_with_memory()
    
    # Get answer from QA chain with memory - NOTE: different input format!
    result = qa_chain_memory.invoke({"question": question})

    # Get answer from QA chain
    # result = ask_gdpr_question.qa_chain.invoke({"query": question})
    
    # Prepare response - NOTE: key changed from 'result' to 'answer'
    response = {
        "answer": result.get('answer', '').strip(),  # Changed key
        "sources": [],
        "memory_count": len(memory_instance.chat_memory.messages) // 2
    }
    
    # Extract sources if requested (same logic as before)
    if show_sources and result.get('source_documents'):
        for doc in result['source_documents']:
            source_text = doc.page_content.strip()
            metadata = doc.metadata or {}
            raw_page = metadata.get('page_number')
            page = None
            if raw_page is not None:
                page = int(float(raw_page))
            else:
                page = raw_page
            document_name = metadata.get('document_name')
            response["sources"].append({
                "content": source_text,
                "page": page,
                "document": document_name,
                "metadata": metadata
            })
    
    return response

def clear_memory():
    """
    Clear the conversation memory
    """
    global memory_instance
    if memory_instance is not None:
        memory_instance.clear()

def get_memory_state():
    """
    Get current memory state for debugging
    """
    global memory_instance
    if memory_instance is not None:
        return {
            "message_count": len(memory_instance.chat_memory.messages),
            "messages": memory_instance.chat_memory.messages
        }
    return {"message_count": 0, "messages": []}

# ---------------------------
#  Ask a question and return answer
# ---------------------------
def ask_gdpr_question(question, show_sources=True):
    """
    Ask a question and return answer with sources
    """
    # Check if API keys are available
    if not OPENAI_API_KEY or not PINECONE_API_KEY:
        return {
            "answer": "❌ API keys not configured. Please set OPENAI_API_KEY and PINECONE_API_KEY in Streamlit secrets.",
            "sources": []
        }
    
    if "qa_chain" not in ask_gdpr_question.__dict__:
        ask_gdpr_question.qa_chain = create_qa_chain()
    
    # Get answer from QA chain
    result = ask_gdpr_question.qa_chain.invoke({"query": question})
    
    # Prepare response
    response = {
        "answer": result.get('result', '').strip(),
        "sources": []
    }
    
    # Extract sources if requested
    if show_sources and result.get('source_documents'):
        for doc in result['source_documents']:
            # Preserve original formatting (newlines)
            source_text = doc.page_content.strip()
            metadata = doc.metadata or {}
            raw_page = metadata.get('page_number')
            # Normalize page to an integer if possible
            page = None
            if raw_page is not None:
                page = int(float(raw_page))
            else:
                page = raw_page
            document_name = metadata.get('document_name')
            response["sources"].append({
                "content": source_text,
                "page": page,
                "document": document_name,
                "metadata": metadata
            })
    
    return response

# Initialize on import
# KEEP your existing initialization:
# qa_chain = create_qa_chain()

# Global variables for memory-based QA chain
qa_chain_memory = None
memory_instance = None
