# GDPR Compliance Assistant for Craftspeople

![Project Status](https://img.shields.io/badge/Status-POC%201-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![LangChain](https://img.shields.io/badge/LangChain-0.2.12-orange)

A multilingual Retrieval-Augmented Generation (RAG) system that helps craftspeople and small businesses understand GDPR compliance requirements through natural language conversations.

## 📖 Project Overview

This project creates an intelligent assistant that can answer data protection questions specifically tailored for craftspeople and small businesses. The system uses German GDPR guidelines and can handle questions in both English and German.

### Data Sources

**Primary Datasets**:

1. **ZDH Data Protection Guide for Crafts Businesses** ([Download PDF](https://www.zdh.de/ueber-uns/fachbereich-organisation-und-recht/datenschutz/datenschutz-fuer-handwerksbetriebe/))
   - **Description**: Comprehensive GDPR guidelines specifically designed for craftspeople and small businesses in Germany. Covers practical implementation of data protection rules with sector-specific examples and recommendations.
   - **Author**: Dr. Markus Peifer, Head of Organization and Law Department, ZDH (Zentralverband des Deutschen Handwerks - Central Association of German Skilled Trades)

2. **BITKOM AI & Data Protection - Practical Guide 2.0** ([Download PDF](https://www.bitkom.org/Bitkom/Publikationen/KI-Datenschutz-Praxisleitfaden))
   - **Description**: The second edition of the "AI & Data Protection" practical guide serves as a comprehensive reference for companies and organizations that want to use and implement AI technologies in compliance with data protection regulations. It provides practical instructions, legal foundations, and concrete tools to ensure that the processing of personal data is in line with GDPR and other relevant regulations.
   - **Key Features**: Contains definitions, instructions, and practice-oriented checklists. Specifically addresses data protection requirements and ethical questions when using AI systems. Includes detailed examples and implementation tips for data protection-compliant AI implementation.
   - **Organization**: BITKOM is Germany's most important digital association and largest European think tank for digital topics, with over 2,200 member companies including SMEs, tech startups, and DAX corporations.

**Key Topics Covered**:
- Basic data protection principles for small businesses
- Customer data handling requirements
- Employee data management
- Data retention periods
- Marketing and consent rules
- Data breach procedures
- AI-specific data protection requirements
- Ethical AI implementation
- Practical implementation guidance

## 🚀 Project Roadmap

### Phase 1: Proof of Concept (POC)
- **POC 1** ✅: Ask questions in German, receive answers in German
- **POC 2** ✅: Ask questions in English or German, receive answers in the same language

### Phase 2: Minimum Viable Product (MVP)
- **MVP 1** ✅: **Web interface with chatbot functionality** - Live at: `www.[fill later]`
- **MVP 2** ✅: **Enhanced knowledge base with AI & Data Protection guidelines** - BITKOM guide integrated

### Future Enhancements
- Multi-document search and comparison
- Conversation memory and follow-up questions
- Enhanced deployment as a web service
- Additional specialized guidelines

## 🛠️ Technical Stack

- **Framework**: LangChain
- **Vector Database**: Pinecone
- **Embeddings**: "text-embedding-3-small" Sentence Transformers (multilingual)
- **Language Model**: OpenAI GPT / Hugging Face models
- **Web Interface**: Streamlit
- **Language Support**: German & English

## 📁 Project Structure

```
gdpr_compliance_assistant/
├── notebooks/ # Jupyter notebooks for development
│   ├── 01_pdf_processing.ipynb    # Process PDF → chunks
│   ├── 02_pinecone_upload.ipynb   # Upload to Pinecone (run once)
│   └── 03_rag_agent.ipynb         # Build RAG (uses existing index)
│   └── 04_pinecone_upload_new_documents.ipynb         # Process (modular) PDF → chunks → Pinecone.
├── data/
│   ├── raw/ # Original PDF documents
│   └── processed/ # Processed chunks and vector database
├── src/ # Source code for the application
├── tests/ # Test files
└── docs/ # Documentation
```

## 🎯 Key Features

- **Multilingual Support**: Questions and answers in German and English
- **Context-Aware Answers**: Based on official craftspeople and AI guidelines
- **Live Web Interface**: Accessible via Streamlit deployment
- **Dual Knowledge Base**: Combines traditional GDPR and AI-specific data protection

## 📊 Data Processing

The system processes PDF documents through:
1. **Text Extraction**: Automatic extraction from German PDFs
2. **Intelligent Chunking**: Semantic splitting with meaningful metadata
3. **Multilingual Embeddings**: Vector representations for semantic search
4. **RAG Pipeline**: Combines retrieval with generative AI

## 🌐 Live Demo

The MVP is now live and accessible at: `www.[fill later]`

**Current Features**:
- Interactive chatbot interface
- Support for both English and German queries
- Answers based on ZDH crafts business guidelines
- Additional AI data protection knowledge from BITKOM
- Real-time response generation

## 🤝 Contributing

This project is developed as part of a data science learning journey. Contributions and suggestions are welcome!

## ⚖️ Disclaimer

This assistant provides general guidance based on official documentation but does not constitute legal advice. For specific legal questions, consult with qualified legal professionals or local trade organizations (Handwerkskammern, Innungen, Fachverbände).

## 📄 License

This project is for educational purposes. The source documents are property of their respective organizations (ZDH, BITKOM).

## 📞 Contact

For questions about this project or suggestions for improvement, please open an issue in the repository.

---

**Built with ❤️ for craftspeople and other bussiness navigating data protection regulations in Germany**


------------------
