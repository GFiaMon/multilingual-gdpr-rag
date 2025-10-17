# backend.py
import streamlit as st
from dotenv import load_dotenv
import os
import time

# 1. Import necessary libraries

# from pinecone import Pinecone, ServerlessSpec
from pinecone import Pinecone

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
# from langchain.agents import Tool, initialize_agent

# for memory in the chat
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain

from langsmith import Client
from langsmith import traceable

from langchain.callbacks.tracers.langchain import wait_for_all_tracers
from langchain.callbacks.manager import collect_runs


# Add this instead:
from langsmith import run_trees

# @st.cache_resource
# def get_langsmith_client():
#     """Initialize LangSmith client once"""
#     return Client()

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
            os.environ["LANGSMITH_PROJECT"] = st.secrets.get("LANGSMITH_PROJECT", "GDPR-Compliance-Assistant")
            
            return True
    else:
        print("⚠️  LangSmith API key not found - tracing disabled")
        return False
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
    prompt_template_mem = """You are a compliance assistant specialized in GDPR and AI data protection for German craft businesses, small businesses, and general knowledge for larger enterprises.
Use the following context and conversation history to answer the question. 
Explain in a clear, practical way. This is not legal advice. If the context does not contain the answer, say so openly and propose a possible alternative question.

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

from langchain.callbacks.manager import collect_runs

def ask_gdpr_question_with_memory(question: str, show_sources: bool = True) -> dict:
    """Get GDPR response with memory and capture run_id for feedback"""
    try:
        with collect_runs() as callback_manager:
            # Your existing chain invocation
            result = your_chain.invoke(
                {"question": question},
                config={"callbacks": [callback_manager]}
            )
            
            # Capture the run_id from the traced run
            run_id = None
            if callback_manager.traced_runs:
                run_id = str(callback_manager.traced_runs[0].id)
            
            return {
                "answer": result.get("answer", "No answer generated"),
                "sources": result.get("sources", []),
                "run_id": run_id  # This is critical for feedback
            }
            
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "sources": [],
            "run_id": None
        }


def ask_gdpr_question_with_memory(question, show_sources=True):
    """
    Ask a question with conversation memory and return answer with sources
    Includes LangSmith run_id for feedback tracking
    """
    global qa_chain_memory, memory_instance
    
    # Check if API keys are available
    if not OPENAI_API_KEY or not PINECONE_API_KEY:
        return {
            "answer": "❌ API keys not configured. Please set OPENAI_API_KEY and PINECONE_API_KEY in Streamlit secrets.",
            "sources": [],
            "memory_count": 0,
            "run_id": None
        }
    
    # Initialize chain and memory if not already done
    if qa_chain_memory is None or memory_instance is None:
        qa_chain_memory, memory_instance = create_qa_chain_with_memory()
    
    # Use collect_runs to properly capture run_id
    current_run_id = None
    try:
        with collect_runs() as callback_manager:
            # Get answer from QA chain with memory
            result = qa_chain_memory.invoke(
                {"question": question},
                config={"callbacks": [callback_manager]}
            )
            
            # Capture run_id from the traced run
            if callback_manager.traced_runs:
                current_run_id = str(callback_manager.traced_runs[0].id)
                
    except Exception as e:
        print(f"Error in QA chain invocation: {e}")
        return {
            "answer": f"❌ Error processing your question: {str(e)}",
            "sources": [],
            "memory_count": 0,
            "run_id": None
        }
    
    # Prepare response with run_id - PRESERVING YOUR EXACT SOURCE FORMAT
    response = {
        "answer": result.get('answer', '').strip(),
        "sources": [],
        "memory_count": len(memory_instance.chat_memory.messages) // 2,
        "run_id": current_run_id  # Add run_id to response
    }
    
    # Extract sources if requested - EXACTLY AS YOU HAD IT
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

# Global variables for memory-based QA chain
qa_chain_memory = None
memory_instance = None

# ---------------------------
#  FEEDBACK to LangSmith
# ---------------------------

def submit_feedback_to_langsmith(run_id: str, score: int, comment: str = "") -> bool:
    """Submit feedback to LangSmith with proper error handling"""
    try:
        if not run_id:
            print("❌ No run_id provided for feedback")
            return False
            
        client = Client()
        
        # Submit feedback
        client.create_feedback(
            run_id=run_id,
            key="user_rating", 
            score=score,  # 1 for thumbs up, 0 for thumbs down
            comment=comment,
            value=str(score)
        )
        
        print(f"✅ Feedback submitted for run_id: {run_id}, score: {score}")
        return True
        
    except Exception as e:
        print(f"❌ LangSmith feedback error: {str(e)}")
        return False
