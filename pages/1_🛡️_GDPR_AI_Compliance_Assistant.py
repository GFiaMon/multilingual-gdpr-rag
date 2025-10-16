import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
import os
import time
import json
import html
from datetime import datetime
from utils import export_chat

# Load environment variables
load_dotenv()

# from backend import ask_gdpr_question, ask_gdpr_question_with_memory, clear_memory, get_memory_state
from backend import ask_gdpr_question_with_memory, clear_memory, get_memory_state
# feedback:
from backend import submit_feedback_to_langsmith

# Set page config
st.set_page_config(
    page_title="GDPR Compliance Assistant",
    page_icon="🛡️",
    layout="centered"
)

# Title and description
st.title("🛡️ GDPR Compliance Assistant")
# st.markdown("Ask questions about data protection for craftspeople and small businesses.")

with st.expander("Hello!", expanded=False):
    st.markdown("""
    Welcome to your multilingual GDPR & AI compliance assistant for **Germany**! This tool helps craftspeople
    and small businesses understand data protection requirements for both traditional operations 
    and AI systems in a practical, easy-to-understand way.

    **Ask questions in English or German** (limited testing for other languages) about:
    """)
    # Create two columns for the bullet points
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        📊 GDPR compliance  
        🤖 AI data protection  
        👥 Customer data
        """)

    with col2:
        st.markdown("""
        👨‍💼 Employee data  
        ⏰ Retention periods  
        🚨 Breach procedures
        """)

    st.info("""
    💡 **Tip:** Answers are provided in the language you ask, but source documents remain in their original German.
    """)

# Disclaimer Expander
with st.expander("ℹ️ Important Disclaimer", expanded=False):
    st.markdown("""
    ⚠️ **This is not legal advice**
    
    This assistant provides general guidance based on official ZDH and BITKOM documentation, 
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
# Initialize feedback tracking
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = {}




# Sidebar: List chats and create new chat
with st.sidebar:
    # First, handle new chat creation before instantiating the selectbox
    chat_names = list(st.session_state.chats.keys())

    # === CHANGE 2: Move selectbox to top ===
    st.subheader("💬 Chat Sessions")                            # <-- Change
    selected_chat = st.selectbox("Select a chat", chat_names, key="current_chat", label_visibility="collapsed")      # <-- Change   

    
    if st.button("New Chat", use_container_width=True):
        new_chat_name = f"Chat {len(chat_names) + 1}"
        st.session_state.chats[new_chat_name] = []
        st.session_state.current_chat = new_chat_name
        st.rerun()
    
    # Optional toggle to display chat count
    if st.toggle("Show chat count", value=False, key="show_chat_count"):
        st.caption(f"Total chats: {len(chat_names)}")
    
    # Rename current chat before creating the selectbox to avoid mutation-after-instantiation
    proposed_name = st.text_input(
        "Rename current chat",
        value=st.session_state.current_chat,
        key="rename_current_chat_input",
    ).strip()
    
    if st.button("Rename", use_container_width=True):
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
    if st.button("🗑️ Delete Chat", use_container_width=True):
        current = st.session_state.current_chat
        if len(st.session_state.chats) <= 1:
            st.warning("Cannot delete the only remaining chat.")
        else:
            # Remove current chat and select another existing one
            st.session_state.chats.pop(current, None)
            remaining_names = list(st.session_state.chats.keys())
            st.session_state.current_chat = remaining_names[0]
            st.rerun()

    # Memory controls
    st.markdown("---")
    st.markdown("**🧠 Memory Controls**")
    
    # Show memory state
    memory_state = get_memory_state()
    st.caption(f"Memory: {memory_state['message_count']} messages")
    
    # Clear memory button
    if st.button("🧹 Clear Memory", use_container_width=True):
        clear_memory()
        st.success("Memory cleared!")
        st.rerun()
    
    # Export current chat download
    current_chat_name = st.session_state.current_chat
    if st.session_state.chats[current_chat_name]:  # Only show download if there are messages
        export_bytes, export_filename = export_chat(
            current_chat_name,
            st.session_state.chats[current_chat_name],
            project_description="GDPR & AI Compliance Assistant - Chat export",
            author="Guillermo Fiallo-Montero",
            url="https://github.com/GFiaMon/multilingual-gdpr-rag",
        )
        st.download_button(
            label="⬇️ Download chat TXT",
            data=export_bytes,
            file_name=export_filename,
            mime="text/plain",
            use_container_width=True,
        )
    else:
        st.caption("No messages to export")
    
    # Add your name at the bottom
    st.caption("---")
    st.caption("👨‍💻 Developer")
    st.caption("**Guillermo Fiallo Montero**")
    # Optional: Add links
    st.caption("[LinkedIn](https://www.linkedin.com/in/guillermo-fiallo-montero-734a87132/) • [GitHub](https://github.com/GFiaMon)")

# Main area: Display messages for the selected chat
st.markdown(f"### {st.session_state.current_chat}")

messages = st.session_state.chats[st.session_state.current_chat]

# for msg in messages:
for idx, msg in enumerate(messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Copy-to-clipboard for assistant messages (includes sources if available)
        if msg["role"] == "assistant":
            _answer_text = (msg.get("content") or "")
            _sources = msg.get("sources") or []
            if _sources:
                _sources_lines = []
                for i, source in enumerate(_sources):
                    _doc_name = source.get("document") or (source.get("metadata", {}) or {}).get("document_name")
                    _page_num = source.get("page") or (source.get("metadata", {}) or {}).get("page_number") or (source.get("metadata", {}) or {}).get("page")
                    _header = f"[{i+1}] {(_doc_name or 'Unknown document')}" + (f" — page {_page_num}" if _page_num is not None else "")
                    _body = (source.get('content', '') or '')
                    _sources_lines.append(f"{_header}\n{_body}")
                _copy_plain = _answer_text + "\n\nSources:\n" + "\n\n".join(_sources_lines)
            else:
                _copy_plain = _answer_text
            _suffix = str(int(time.time() * 1000))
            _escaped_html = html.escape(_copy_plain)
            components.html(
                """
                <div style=\"display:flex; justify-content:flex-end; margin: 4px 0;\">
                  <button id=\"copy-btn-""" + _suffix + """\" style=\"font-size:12px; padding:4px 8px; cursor:pointer;\">📋 Copy</button>
                </div>
                <textarea id=\"copy-text-""" + _suffix + """\" style=\"position:absolute; left:-10000px; top:-10000px; white-space:pre;\">""" + _escaped_html + """</textarea>
                <script>
                (function(){
                  var btn = document.getElementById('copy-btn-""" + _suffix + """');
                  var txt = document.getElementById('copy-text-""" + _suffix + """');
                  if(btn && txt){
                    btn.addEventListener('click', async function(){
                      try{
                        await navigator.clipboard.writeText(txt.value);
                        btn.textContent = '✅ Copied';
                        setTimeout(function(){ btn.textContent = '📋 Copy'; }, 1200);
                      }catch(e){
                        btn.textContent = '⚠️ Failed';
                      }
                    });
                  }
                })();
                </script>
                """,
                height=50,
            )

            # === CHANGE 1: Add feedback buttons for assistant messages ===
            col_fb1, col_fb2, col_fb3 = st.columns([1, 1, 6])
            with col_fb1:
                if st.button("👍", key=f"thumbs_up_{idx}", use_container_width=True):
                    run_id = msg.get("run_id")
                    if run_id:
                        success = submit_feedback_to_langsmith(run_id, 1, "User liked this response")
                        if success:
                            st.success("✅ Thanks for your feedback!")
                        else:
                            st.error("❌ Failed to submit feedback")
                    else:
                        st.warning("⚠️ No run_id available for feedback")
            with col_fb2:
                if st.button("👎", key=f"thumbs_down_{idx}", use_container_width=True):
                    run_id = msg.get("run_id")
                    if run_id:
                        success = submit_feedback_to_langsmith(run_id, 0, "User disliked this response")
                        if success:
                            st.success("✅ Thanks for your feedback!")
                        else:
                            st.error("❌ Failed to submit feedback")
                    else:
                        st.warning("⚠️ No run_id available for feedback")



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
    messages.append({"role": "user", "content": prompt, "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        # Show thinking indicator
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown("🤔 Thinking...")
        
        # Get response from backend
        
        # # To use memory version, simply change this line in your app:
        # # FROM (no memory):
        # response = ask_gdpr_question(prompt, show_sources=True)

        # # TO (with memory):
        response = ask_gdpr_question_with_memory(prompt, show_sources=True)


        # Display answer
        thinking_placeholder.markdown(response["answer"])
        
        # Copy-to-clipboard button for the latest assistant answer (includes sources if available)
        _latest_answer = response.get("answer") or ""
        _latest_sources = response.get("sources") or []
        if _latest_sources:
            _latest_sources_lines = []
            for i, source in enumerate(_latest_sources):
                _doc_name = source.get("document") or (source.get("metadata", {}) or {}).get("document_name")
                _page_num = source.get("page") or (source.get("metadata", {}) or {}).get("page_number") or (source.get("metadata", {}) or {}).get("page")
                _header = f"[{i+1}] {(_doc_name or 'Unknown document')}" + (f" — page {_page_num}" if _page_num is not None else "")
                _body = (source.get('content', '') or '')
                _latest_sources_lines.append(f"{_header}\n{_body}")
            _copy_latest_plain = _latest_answer + "\n\nSources:\n" + "\n\n".join(_latest_sources_lines)
        else:
            _copy_latest_plain = _latest_answer
        _suffix2 = str(int(time.time() * 1000))
        _escaped_html_resp = html.escape(_copy_latest_plain)
        components.html(
            """
            <div style=\"display:flex; justify-content:flex-end; margin: 4px 0;\">
              <button id=\"copy-btn-""" + _suffix2 + """\" style=\"font-size:12px; padding:4px 8px; cursor:pointer;\">📋 Copy</button>
            </div>
            <textarea id=\"copy-text-""" + _suffix2 + """\" style=\"position:absolute; left:-10000px; top:-10000px; white-space:pre;\">""" + _escaped_html_resp + """</textarea>
            <script>
            (function(){
              var btn = document.getElementById('copy-btn-""" + _suffix2 + """');
              var txt = document.getElementById('copy-text-""" + _suffix2 + """');
              if(btn && txt){
                btn.addEventListener('click', async function(){
                  try{
                    await navigator.clipboard.writeText(txt.value);
                    btn.textContent = '✅ Copied';
                    setTimeout(function(){ btn.textContent = '📋 Copy'; }, 1200);
                  }catch(e){
                    btn.textContent = '⚠️ Failed';
                  }
                });
              }
            })();
            </script>
            """,
            height=50,
        )

        # === CHANGE 1: Add feedback buttons for the latest response ===
        col_fb1, col_fb2, col_fb3 = st.columns([1, 1, 6])
        with col_fb1:
            if st.button("👍", key="thumbs_up_latest", use_container_width=True):
                run_id = response.get("run_id")
                if run_id:
                    success = submit_feedback_to_langsmith(run_id, 1, "User liked this response")
                    if success:
                        st.success("✅ Thanks for your feedback!")
                    else:
                        st.error("❌ Failed to submit feedback")
                else:
                    st.warning("⚠️ No run_id available for feedback")
        with col_fb2:
            if st.button("👎", key="thumbs_down_latest", use_container_width=True):
                run_id = response.get("run_id")
                if run_id:
                    success = submit_feedback_to_langsmith(run_id, 0, "User disliked this response")
                    if success:
                        st.success("✅ Thanks for your feedback!")
                    else:
                        st.error("❌ Failed to submit feedback")
                else:
                    st.warning("⚠️ No run_id available for feedback")

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
    messages.append({
        "role": "assistant",
        "content": response["answer"],
        "sources": response["sources"],
        "run_id": response.get("run_id"),  # Add this line to store the run_id
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    })
    # Persist back to session state (not strictly necessary but explicit)
    st.session_state.chats[st.session_state.current_chat] = messages