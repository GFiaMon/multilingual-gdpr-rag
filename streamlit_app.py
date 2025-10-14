# app.py - Most Basic GDPR Chatbot
import streamlit as st
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

from backend import ask_gdpr_question

# import sys
# # Add project root to Python path
# sys.path.append(os.path.abspath('..'))

# # LangChain components
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # ✅ Correct imports
# from langchain_pinecone import PineconeVectorStore  # ✅ Pinecone integration
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate

# from pinecone import Pinecone, ServerlessSpec


# Set page config
st.set_page_config(
    page_title="GDPR Compliance Assistant",
    page_icon="🛡️",
    layout="centered"
)

# Title and description
st.title("🛡️ GDPR Compliance Assistant")
st.markdown("Ask questions about data protection for craftspeople and small businesses.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# # Display chat messages (1st version)
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources for assistant messages
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📚 Source Documents"):
                for i, source in enumerate(message["sources"]):
                    st.markdown(f"**Source {i+1}:**")
                    st.markdown(f"{source['content'][:200]}...")
                    st.markdown("---")


# Chat input
if prompt := st.chat_input("Ask about GDPR compliance..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        # Show thinking indicator
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown("🤔 Thinking...")
        
        # Get response from backend
        response = ask_gdpr_question(prompt, show_sources=True)
        
        # Display answer
        thinking_placeholder.markdown(response["answer"])
        
        # Display sources in expander
        if response["sources"]:
            with st.expander(f"📚 Source Documents ({len(response['sources'])})"):
                for i, source in enumerate(response["sources"]):
                    st.markdown(f"**Source {i+1}:**")
                    st.markdown(f"{source['content'][:300]}...")
                    st.markdown("---")
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response["answer"],
        "sources": response["sources"]
    })


# # Chat input (1st version)
# if prompt := st.chat_input("Ask about GDPR compliance..."):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Display assistant response
#     with st.chat_message("assistant"):
#         # SIMPLE RESPONSE - Replace this with your actual RAG agent later
#         placeholder = st.empty()
#         placeholder.markdown("🤔 Thinking...")
        
#         # TODO: Replace this with your actual RAG agent call
#         response = f"I received your question: '{prompt}'. This is where the RAG agent will answer."
        
#         placeholder.markdown(response)
    
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})