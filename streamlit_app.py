# app.py - Most Basic GDPR Chatbot
import streamlit as st
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

from backend import ask_gdpr_question

# Set page config
st.set_page_config(
    page_title="GDPR Compliance Assistant",
    page_icon="🛡️",
    layout="centered"
)

# Title and description
st.title("🛡️ GDPR Compliance Assistant")
# st.markdown("Ask questions about data protection for craftspeople and small businesses.")

st.markdown("""
Welcome to your multilingual GDPR assistant! This tool helps craftspeople and small businesses 
understand data protection requirements in a practical, easy-to-understand way.

**Ask questions in English or German** about:
""")
# Create two columns for the bullet points
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - Data processing principles
    - Employee data management  
    - Customer data handling
    """)

with col2:
    st.markdown("""
    - Data retention periods
    - Surveillance and monitoring
    - Data breach procedures
    """)

# Disclaimer Expander
with st.expander("ℹ️ Important Disclaimer", expanded=True):
    st.markdown("""
    ⚠️ **This is not legal advice**
    
    This assistant provides general guidance based on official GDPR documentation for craftspeople, 
    but it does not constitute legal advice. For specific legal questions or complex situations, 
    please consult with qualified legal professionals or your local trade organizations 
    (Handwerkskammern, Innungen, Fachverbände).
    
    🔄 **Service Limitations**
    
    We appreciate your engagement! Please note, this demo is designed to process a maximum of 
    10 interactions and may be unavailable if too many people use the service concurrently. 
    Thank you for your understanding.
    """)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources for assistant messages
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📚 Source Documents"):
                for i, source in enumerate(message["sources"]):
                    doc_name = source.get("document") or (source.get("metadata", {}) or {}).get("document_name")
                    page_num = source.get("page") or (source.get("metadata", {}) or {}).get("page_number") or (source.get("metadata", {}) or {}).get("page")
                    header = f"**Source {i+1}:** {doc_name or 'Unknown document'}"
                    if page_num is not None:
                        header += f" — page {page_num}"
                    st.markdown(header)
                    # Preserve original line breaks in normal font
                    st.markdown((source.get('content', '') or '').replace('\n', '  \n'))
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
                    doc_name = source.get("document") or (source.get("metadata", {}) or {}).get("document_name")
                    page_num = source.get("page") or (source.get("metadata", {}) or {}).get("page_number") or (source.get("metadata", {}) or {}).get("page")
                    header = f"**Source {i+1}:** {doc_name or 'Unknown document'}"
                    if page_num is not None:
                        header += f" — page {page_num}"
                    st.markdown(header)
                    # Preserve original line breaks in normal font
                    st.markdown((source.get('content', '') or '').replace('\n', '  \n'))
                    st.markdown("---")
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response["answer"],
        "sources": response["sources"]
    })