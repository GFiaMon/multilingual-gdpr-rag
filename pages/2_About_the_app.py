import streamlit as st

# Page configuration
st.set_page_config(
    page_title="GDPR Compliance Assistant",
    page_icon="ℹ️",
    layout="wide"
)

# Header section
st.title("ℹ️ About the GDPR Compliance Assistant")

# Social links with simple badges
st.write("""
[![LinkedIn Profile](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://www.linkedin.com/in/guillermo-fiallo-montero-734a87132/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Source-181717?logo=github)](https://github.com/GFiaMon/multilingual-gdpr-rag)
made by     **Guillermo Fiallo-Montero**
""")

st.divider()

# Main description
st.markdown("""
**A multilingual AI assistant that helps craftspeople and small businesses navigate GDPR compliance 
and AI data protection requirements through natural language conversations.**
""")

# Features section
st.subheader("🚀 Key Features")
st.divider()

col1, col2 = st.columns(2)
st.markdown("<br>", unsafe_allow_html=True)

with col1:
    with st.container(border=True):
        st.markdown("#### 🌐 Multilingual Support")
        st.markdown("Ask questions in **English or German** and receive answers in the same language. Perfect for international crafts businesses operating in Germany.")
    
    with st.container(border=True):
        st.markdown("#### 🛡️ GDPR Compliance Guidance")
        st.markdown("Get practical answers about data protection rules specifically tailored for crafts businesses, based on official ZDH guidelines.")

with col2:
    with st.container(border=True):
        st.markdown("#### 🤖 AI Data Protection")
        st.markdown("Understand data protection requirements for AI systems with guidance from BITKOM's comprehensive AI & Data Protection practical guide.")
    
    with st.container(border=True):
        st.markdown("#### 🔍 Context-Aware Answers")
        st.markdown("Receive accurate, context-specific responses powered by Retrieval-Augmented Generation (RAG) technology and official documentation.")

# Add spacing before the next section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# Data sources section - Perfect balance
col_left, col_center, col_right = st.columns([0.5, 3, 0.5])
with col_center:
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>📚 Knowledge Base</h3>", unsafe_allow_html=True)
        st.markdown("""
        Our assistant is powered by official German guidelines:

        - **ZDH Data Protection Guide for Crafts Businesses** - Practical GDPR implementation for skilled trades
        - **BITKOM AI & Data Protection Practical Guide 2.0** - Comprehensive AI compliance framework
        """)

# Add spacing
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# How to use section
col_left, col_center, col_right = st.columns([0.5, 3, 0.5])
with col_center:
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>💡 How to Use</h3>", unsafe_allow_html=True)
        st.markdown("""
        1. **Navigate to the Chat page** using the sidebar
        2. **Choose your language** - English or German
        3. **Ask your question** about GDPR compliance, data protection, or AI regulations
        4. **Get instant, reliable answers** based on official guidelines
        """)

# Add spacing
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Technology stack
col_left, col_center, col_right = st.columns([0.5, 3, 0.5])
with col_center:
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>🛠️ Built With</h3>", unsafe_allow_html=True)
        st.markdown("""
        - **LangChain** - AI framework for RAG pipeline
        - **Pinecone** - Vector database for semantic search  
        - **OpenAI GPT** - Language model for response generation
        - **Streamlit** - Web interface deployment
        - **Multilingual Embeddings** - Support for English and German
        """)

# Optional: Add some metrics or app info
col_left, col_center, col_right = st.columns([0.5, 3, 0.5])
with col_center:
    with st.expander("📊 App Information"):
        st.markdown("""
        **Version**: 1.0 \n
        October 2025
        """)    

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B7280;'>
    <p><i>This tool provides general guidance based on official documentation. For specific legal advice, consult qualified professionals.</i></p>
    <p><i>Developed as part of a Data Science learning journey</i></p>
</div>
""", unsafe_allow_html=True)

# Footer in main content area
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <p><strong>👨‍💻 Developed by Guillermo Fiallo Montero</strong></p>
        <p>
            <a href="https://www.linkedin.com/in/guillermo-fiallo-montero-734a87132/" target="_blank">LinkedIn</a> • 
            <a href="https://github.com/GFiaMon" target="_blank">GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)