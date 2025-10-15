import streamlit as st

# Page configuration
st.set_page_config(
    page_title="GDPR Compliance Assistant",
    page_icon="🛡️",
    layout="wide"
)

# Header section
st.title("GDPR Compliance Assistant for Craftspeople")


# Social links with simple badges
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown("[![GitHub Repository](https://img.shields.io/badge/GitHub-View_Source-181717?logo=github)](https://github.com/GFiaMon/multilingual-gdpr-rag)")
with col3:
    st.markdown("[![LinkedIn Profile](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://www.linkedin.com/in/guillermo-fiallo-montero-734a87132/)")

st.divider()

# Main description
st.markdown("""
**A multilingual AI assistant that helps craftspeople and small businesses navigate GDPR compliance 
and AI data protection requirements through natural language conversations.**
""")

# Features section
st.subheader("🚀 Key Features")

col1, col2 = st.columns(2)

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

# Data sources section
st.subheader("📚 Knowledge Base")
st.markdown("""
Our assistant is powered by official German guidelines:

- **ZDH Data Protection Guide for Crafts Businesses** - Practical GDPR implementation for skilled trades
- **BITKOM AI & Data Protection Practical Guide 2.0** - Comprehensive AI compliance framework
""")

# How to use section
st.subheader("💡 How to Use")
st.markdown("""
1. **Navigate to the Chat page** using the sidebar
2. **Choose your language** - English or German
3. **Ask your question** about GDPR compliance, data protection, or AI regulations
4. **Get instant, reliable answers** based on official guidelines
""")

# Technology stack
st.subheader("🛠️ Built With")
st.markdown("""
- **LangChain** - AI framework for RAG pipeline
- **Pinecone** - Vector database for semantic search  
- **OpenAI GPT** - Language model for response generation
- **Streamlit** - Web interface deployment
- **Multilingual Embeddings** - Support for English and German
""")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B7280;'>
    <p><i>This tool provides general guidance based on official documentation. For specific legal advice, consult qualified professionals.</i></p>
    <p><i>Developed as part of a Data Science learning journey</i></p>
</div>
""", unsafe_allow_html=True)



# /////////

# import streamlit as st

# # Page configuration
# st.set_page_config(
#     page_title="GDPR Compliance Assistant",
#     page_icon="🛡️",
#     layout="wide"
# )

# # Custom CSS for white theme alignment
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         color: #1E3A8A;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
#     .sub-header {
#         font-size: 1.2rem;
#         color: #4B5563;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .feature-card {
#         background-color: white;
#         padding: 1.5rem;
#         border-radius: 10px;
#         margin: 1rem 0;
#         border-left: 4px solid #1E3A8A;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .social-links {
#         display: flex;
#         justify-content: center;
#         gap: 20px;
#         margin: 2rem 0;
#         align-items: center;
#     }
#     .badge-container {
#         display: flex;
#         gap: 10px;
#         align-items: center;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header section
# st.markdown('<h1 class="main-header">GDPR Compliance Assistant for Craftspeople</h1>', unsafe_allow_html=True)

# # Social links bar - centered and properly aligned
# st.markdown("""
# <div class="social-links">
#     <div class="badge-container">
#         <a href="https://github.com/yourusername/gdpr-compliance-assistant" target="_blank">
#             <img src="https://img.shields.io/badge/GitHub-View_Source-181717?logo=github" alt="GitHub">
#         </a>
#         <a href="https://linkedin.com/in/yourprofile" target="_blank">
#             <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin" alt="LinkedIn">
#         </a>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# st.markdown("---")

# # Main description
# st.markdown("""
# <div class="sub-header">
# A multilingual AI assistant that helps craftspeople and small businesses navigate GDPR compliance 
# and AI data protection requirements through natural language conversations.
# </div>
# """, unsafe_allow_html=True)

# # Features section
# st.subheader("🚀 Key Features")

# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("""
#     <div class="feature-card">
#     <h4>🌐 Multilingual Support</h4>
#     Ask questions in <b>English or German</b> and receive answers in the same language. 
#     Perfect for international crafts businesses operating in Germany.
#     </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown("""
#     <div class="feature-card">
#     <h4>🛡️ GDPR Compliance Guidance</h4>
#     Get practical answers about data protection rules specifically tailored for 
#     crafts businesses, based on official ZDH guidelines.
#     </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.markdown("""
#     <div class="feature-card">
#     <h4>🤖 AI Data Protection</h4>
#     Understand data protection requirements for AI systems with guidance from 
#     BITKOM's comprehensive AI & Data Protection practical guide.
#     </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown("""
#     <div class="feature-card">
#     <h4>🔍 Context-Aware Answers</h4>
#     Receive accurate, context-specific responses powered by Retrieval-Augmented 
#     Generation (RAG) technology and official documentation.
#     </div>
#     """, unsafe_allow_html=True)

# # Data sources section
# st.subheader("📚 Knowledge Base")
# st.markdown("""
# Our assistant is powered by official German guidelines:

# - **ZDH Data Protection Guide for Crafts Businesses** - Practical GDPR implementation for skilled trades
# - **BITKOM AI & Data Protection Practical Guide 2.0** - Comprehensive AI compliance framework
# """)

# # How to use section
# st.subheader("💡 How to Use")
# st.markdown("""
# 1. **Navigate to the Chat page** using the sidebar
# 2. **Choose your language** - English or German
# 3. **Ask your question** about GDPR compliance, data protection, or AI regulations
# 4. **Get instant, reliable answers** based on official guidelines
# """)

# # Technology stack
# st.subheader("🛠️ Built With")
# st.markdown("""
# - **LangChain** - AI framework for RAG pipeline
# - **Pinecone** - Vector database for semantic search  
# - **OpenAI GPT** - Language model for response generation
# - **Streamlit** - Web interface deployment
# - **Multilingual Embeddings** - Support for English and German
# """)

# # Footer
# st.markdown("---")
# st.markdown("""
# <div style='text-align: center; color: #6B7280;'>
#     <p>This tool provides general guidance based on official documentation. For specific legal advice, consult qualified professionals.</p>
#     <p>Developed as part of a Data Science learning journey</p>
# </div>
# """, unsafe_allow_html=True)