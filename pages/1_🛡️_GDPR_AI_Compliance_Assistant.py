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
Welcome to your multilingual GDPR & AI compliance assistant for Germany! This tool helps craftspeople
and small businesses understand data protection requirements for both traditional operations 
and AI systems in a practical, easy-to-understand way.

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
with st.expander("ℹ️ Important Disclaimer", expanded=False):
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

# Initialize chat sessions in session state
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

# Sidebar: List chats and create new chat
with st.sidebar:
    # First, handle new chat creation before instantiating the selectbox
    chat_names = list(st.session_state.chats.keys())
    # Optional toggle to display chat count
    if st.toggle("Show chat count", value=False, key="show_chat_count"):
        st.caption(f"Total chats: {len(chat_names)}")
    if st.button("New Chat"):
        new_chat_name = f"Chat {len(chat_names) + 1}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.current_chat = new_chat_name
        st.rerun()
    # Rename current chat before creating the selectbox to avoid mutation-after-instantiation
    proposed_name = st.text_input(
        "Rename current chat",
        value=st.session_state.current_chat,
        key="rename_current_chat_input",
    ).strip()
    if st.button("Rename"):
        old_name = st.session_state.current_chat
        new_name = proposed_name
        if not new_name:
            st.warning("Chat name cannot be empty.")
        elif new_name == old_name:
            st.info("Name unchanged.")
        elif new_name in st.session_state.chats:
            st.warning("A chat with this name already exists. Choose a different name.")
        else:
            st.session_state.chats[new_name] = st.session_state.chats.pop(old_name)
            st.session_state.current_chat = new_name
            st.rerun()
    # Delete current chat with safeguard; do this before selectbox
    if st.button("🗑️ Delete Chat"):
        current = st.session_state.current_chat
        if len(st.session_state.chats) <= 1:
            st.warning("Cannot delete the only remaining chat.")
        else:
            # Remove current chat and select another existing one
            st.session_state.chats.pop(current, None)
            remaining_names = list(st.session_state.chats.keys())
            st.session_state.current_chat = remaining_names[0]
            st.rerun()
    # Now instantiate the selectbox bound to the updated session state
    selected_chat = st.selectbox("Select a chat", chat_names, key="current_chat")

# Main area: Display messages for the selected chat
st.title(f"Chat: {st.session_state.current_chat}")
messages = st.session_state.chats[st.session_state.current_chat]

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Show sources for assistant messages
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📚 Source Documents"):
                for i, source in enumerate(msg["sources"]):
                    doc_name = source.get("document") or (source.get("metadata", {}) or {}).get("document_name")
                    page_num = source.get("page") or (source.get("metadata", {}) or {}).get("page_number") or (source.get("metadata", {}) or {}).get("page")
                    header = f"**Source {i+1}:** {doc_name or 'Unknown document'}"
                    if page_num is not None:
                        header += f" — page {page_num}"
                    st.markdown(header)
                    st.markdown((source.get('content', '') or '').replace('\n', '  \n'))
                    st.markdown("---")

# Chat input
if prompt := st.chat_input("Ask about GDPR compliance..."):
    # Add user message to chat history
    # st.session_state.messages.append({"role": "user", "content": prompt}) #< working code
    messages.append({"role": "user", "content": prompt})        #new exp code
    
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
    # st.session_state.messages.append({              #< working code
    messages.append({              #< new exp code
        "role": "assistant", 
        "content": response["answer"],
        "sources": response["sources"]
    })
    # Persist back to session state (not strictly necessary but explicit)
    st.session_state.chats[st.session_state.current_chat] = messages