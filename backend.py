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
    Get API keys from Streamlit secrets
    """
    try:
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
        index_name = "gdpr-compliance-openai"
        
        print("✅ Environment setup from Streamlit secrets")
        return index_name, OPENAI_API_KEY, PINECONE_API_KEY
        
    except Exception as e:
        print(f"❌ Error loading secrets: {e}")
        # Fallback for local development
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        index_name = "gdpr-compliance-openai"
        
        if OPENAI_API_KEY and PINECONE_API_KEY:
            print("✅ Environment setup from local environment variables")
            return index_name, OPENAI_API_KEY, PINECONE_API_KEY
        else:
            raise Exception("Please set OPENAI_API_KEY and PINECONE_API_KEY in Streamlit secrets or environment variables")

# Initialize environment
index_name, OPENAI_API_KEY, PINECONE_API_KEY = setup_environment()

# # ---------------------------
# # Configure your API keys (with .env)
# # ---------------------------
# def setup_environment():
#     # Check if API keys are already in environment
#     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#     PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    
#     # If not set, prompt user
#     if not OPENAI_API_KEY:
#         OPENAI_API_KEY = getpass.getpass("Enter your OpenAI API key: ")
#         os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    
#     if not PINECONE_API_KEY:
#         PINECONE_API_KEY = getpass.getpass("Enter your Pinecone API key: ")
#         os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
    
#     # Your Pinecone index name (replace with your actual index name)
#     index_name = "gdpr-compliance-openai"  # Change this to your index name
    
#     return index_name, OPENAI_API_KEY, PINECONE_API_KEY

# # Initialize environment
# index_name, OPENAI_API_KEY, PINECONE_API_KEY = setup_environment()

# ---------------------------
# Pinecone Initialization (Current syntax)
# ---------------------------
def init_pinecone(api_key: str, index_name: str = "gdpr-compliance-openai", environment: str = "us-east-1"):
    """
    Initialize Pinecone connection using current Pinecone
    """
    if not api_key:
        raise ValueError("PINECONE_API_KEY is missing!")
    
    # Initialize Pinecone (Current API)
    print("🔌 Initializing Pinecone...")
    # from pinecone import Pinecone, ServerlessSpec
    pc = Pinecone(api_key=api_key)
    print("✅ Pinecone initialized successfully")
    
    # Check if index exists
    if index_name in pc.list_indexes().names():
        print(f"✅ Index '{index_name}' exists")
        # Wait for index to be ready
        while not pc.describe_index(index_name).status.ready:
            print("⏳ Waiting for index to be ready...")
            # import time
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
    print("🔤 Initializing embeddings...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_API_KEY
    )
    print("✅ Embeddings initialized")
    return embeddings

# ---------------------------
# vector store connection Initialization 
# ---------------------------
def init_vector_store():
    """
    Initialize the vector store connection
    """
    print("🔄 Connecting to vector store...")
    pc, index = init_pinecone(PINECONE_API_KEY)
    embeddings = init_embeddings()
    
    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        text_key="text"
    )
    print("✅ Vector store connected")
    return vector_store

# ---------------------------
# LLM Initialization 
# ---------------------------
def init_llm():
    """
    Initialize the LLM
    """
    print("🧠 Initializing LLM...")
    
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name='gpt-3.5-turbo',
        temperature=0.0,
        max_tokens=500,
    )
    print("✅ LLM initialized")
    return llm

# ---------------------------
# QA Chain Initialization 
# ---------------------------
def create_qa_chain():
    """
    Create the QA chain with English prompt
    """
    print("🔗 Creating QA chain...")
    
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
    
    print("✅ QA chain created")
    return qa_chain_en

# ---------------------------
# QA Memory (opt.)  Initialization 
# ---------------------------

def create_qa_chain_with_memory():
    """Create QA chain with conversation memory"""
    print("🔗 Creating QA chain with memory...")
    
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
        verbose=True  # Set to True to see the chain thinking
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
    
    # Initialize chain and memory if not already done
    if qa_chain_memory is None or memory_instance is None:
        qa_chain_memory, memory_instance = create_qa_chain_with_memory()
    
    # Get answer from QA chain with memory - NOTE: different input format!
    result = qa_chain_memory({"question": question})
    
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
        print("🧹 Memory cleared")

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
            # Preserve original formatting (newlines) from the indexed content
            source_text = doc.page_content.strip()
            metadata = doc.metadata or {}
            raw_page = metadata.get('page_number')  # or metadata.get('page')
            # Normalize page to an integer if possible
            page = None
            if raw_page is not None:
                page = int(float(raw_page))
            else:
                page = raw_page
            document_name = metadata.get('document_name') # or metadata.get('source') or metadata.get('file_name')
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
