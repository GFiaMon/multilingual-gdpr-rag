# GDPR Compliance Assistant for Craftspeople

![Project Status](https://img.shields.io/badge/Status-POC%201-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![LangChain](https://img.shields.io/badge/LangChain-0.2.12-orange)

A multilingual Retrieval-Augmented Generation (RAG) system that helps craftspeople and small businesses understand GDPR compliance requirements through natural language conversations.

## 📖 Project Overview

This project creates an intelligent assistant that can answer data protection questions specifically tailored for craftspeople and small businesses. The system uses German GDPR guidelines and can handle questions in both English and German.

### Data Sources

**Primary Dataset**: 
- **ZDH Data Protection Guide for Crafts Businesses** ([Download PDF](https://www.zdh.de/ueber-uns/fachbereich-organisation-und-recht/datenschutz/datenschutz-fuer-handwerksbetriebe/))
- **Description**: Comprehensive GDPR guidelines specifically designed for craftspeople and small businesses in Germany. Covers practical implementation of data protection rules with sector-specific examples and recommendations.

**Author**: Dr. Markus Peifer, Head of Organization and Law Department, ZDH (Zentralverband des Deutschen Handwerks - Central Association of German Skilled Trades)

**Key Topics Covered**:
- Basic data protection principles for small businesses
- Customer data handling requirements
- Employee data management
- Data retention periods
- Marketing and consent rules
- Data breach procedures
- Practical implementation guidance

## 🚀 Project Roadmap

### Phase 1: Proof of Concept (POC)
- **POC 1** ✅: Ask questions in German, receive answers in German
- **POC 2** 🔄: Ask questions in English or German, receive answers in the same language

### Phase 2: Minimum Viable Product (MVP)
- **MVP 1** 🎯: Web interface with chatbot functionality
- **MVP 2** 📚: Enhanced knowledge base with AI & Data Protection guidelines

### Future Enhancements
- **Additional Dataset**: BITKOM "AI & Data Protection" Practical Guide ([View Details](https://www.bitkom.org/Bitkom/Publikationen/KI-Datenschutz-Praxisleitfaden))
- Multi-document search and comparison
- Conversation memory and follow-up questions
- Deployment as a web service

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
├── data/
│ ├── raw/ # Original PDF documents
│ └── processed/ # Processed chunks and vector database
├── src/ # Source code for the application
├── tests/ # Test files
└── docs/ # Documentation
```

## 🎯 Key Features

- **Multilingual Support**: Questions and answers in German and English
- **Context-Aware Answers**: Based on official craftspeople guidelines

## 📊 Data Processing

The system processes PDF documents through:
1. **Text Extraction**: Automatic extraction from German PDFs
2. **Intelligent Chunking**: Semantic splitting with meaningful metadata
3. **Multilingual Embeddings**: Vector representations for semantic search
4. **RAG Pipeline**: Combines retrieval with generative AI

## 🤝 Contributing

This project is developed as part of a data science learning journey. Contributions and suggestions are welcome!

## ⚖️ Disclaimer

This assistant provides general guidance based on official documentation but does not constitute legal advice. For specific legal questions, consult with qualified legal professionals or local trade organizations (Handwerkskammern, Innungen, Fachverbände).

## 📄 License

This project is for educational purposes. The source documents are property of their respective organizations (ZDH, BITKOM).

## 📞 Contact

For questions about this project or suggestions for improvement, please open an issue in the repository.

---

**Built with ❤️ for craftspeople navigating data protection regulations**


------------------



