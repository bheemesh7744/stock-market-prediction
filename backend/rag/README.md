# RAG System for AI Trader

A Retrieval Augmented Generation (RAG) system that enhances the AI Trader with context-aware responses based on trading strategy documents.

## Overview

The RAG system uses:
- **LangChain** for document processing and embedding
- **ChromaDB** as vector database for similarity search
- **Sentence Transformers** for document embeddings
- **Trading Strategy Documents** as knowledge base

## Structure

```
backend/rag/
├── __init__.py          # Package initialization
├── embed.py            # Document embedding functionality
├── retrieve.py         # Document retrieval functionality  
├── rag_service.py      # Main RAG service integration
├── data/               # Trading strategy documents
│   ├── risk_management.txt
│   ├── technical_indicators.txt
│   ├── trading_strategies.txt
│   └── market_psychology.txt
└── README.md           # This file
```

## Features

### Document Embedding (`embed.py`)
- Loads trading strategy documents from data directory
- Splits documents into manageable chunks
- Creates embeddings using sentence transformers
- Stores embeddings in ChromaDB vector database
- Supports adding new documents dynamically

### Document Retrieval (`retrieve.py`)
- Retrieves top 3 most relevant documents for user queries
- Provides similarity scores for retrieved documents
- Formats retrieved context for LLM consumption
- Creates RAG-enhanced prompts with context

### RAG Service (`rag_service.py`)
- Main integration point for the web application
- Health monitoring and system status
- Document management capabilities
- Query processing with context retrieval

### Knowledge Base Documents
- **Risk Management**: Comprehensive risk management strategies
- **Technical Indicators**: Guide to various technical analysis tools
- **Trading Strategies**: Different trading approaches and methodologies
- **Market Psychology**: Behavioral finance and trading psychology

## Installation

1. Install required dependencies:
```bash
pip install langchain chromadb sentence-transformers transformers torch
```

2. The system will automatically initialize when the web application starts.

## Usage

### Web Interface
1. Start the web application
2. Navigate to `/trading_assistant`
3. Ask questions about trading strategies, risk management, technical analysis, etc.
4. The system will retrieve relevant documents and provide context-aware responses

### API Endpoints

#### Initialize RAG System
```http
POST /api/rag/initialize
```

#### Query Trading Assistant
```http
POST /api/rag/query
Content-Type: application/json

{
    "query": "What are the best risk management strategies?"
}
```

#### Health Check
```http
GET /api/rag/health
```

#### Get Available Documents
```http
GET /api/rag/documents
```

#### Add New Document
```http
POST /api/rag/add_document
Content-Type: application/json

{
    "filename": "new_strategy.txt",
    "content": "Document content here..."
}
```

## Example Queries

- "What are the best risk management strategies?"
- "How do I use RSI indicator for trading?"
- "What is momentum trading strategy?"
- "How should I handle market psychology?"
- "What are the best technical indicators for beginners?"

## Configuration

### Default Settings
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store**: ChromaDB with persistence
- **Chunk Size**: 1000 characters with 200 character overlap
- **Top Documents Retrieved**: 3

### Customization
You can modify settings in the respective files:
- Change embedding model in `embed.py`
- Adjust chunking parameters in `embed.py`
- Modify number of retrieved documents in `retrieve.py`

## Adding New Documents

### Method 1: Add to Data Directory
1. Place new `.txt`, `.md`, or `.json` files in `backend/rag/data/`
2. Reinitialize the RAG system via API or web interface

### Method 2: Use API
```http
POST /api/rag/add_document
Content-Type: application/json

{
    "filename": "custom_strategy.txt",
    "content": "Your trading strategy content..."
}
```

## Monitoring

### Health Check
The system provides comprehensive health monitoring:
- Vector store status
- Document count
- Retrieval functionality
- Service initialization status

### Logging
All operations are logged with appropriate levels:
- INFO: Normal operations
- WARNING: Non-critical issues
- ERROR: System errors

## Performance Considerations

### Embedding Performance
- Initial embedding may take time for large documents
- Subsequent queries are fast due to cached embeddings
- Consider document size for optimal performance

### Memory Usage
- ChromaDB stores embeddings efficiently
- Large document collections may require more memory
- Monitor system resources for large knowledge bases

## Troubleshooting

### Common Issues

1. **Vector Store Not Found**
   - Solution: Initialize the RAG system
   - API: `POST /api/rag/initialize`

2. **No Documents Retrieved**
   - Check if documents exist in data directory
   - Verify document format (.txt, .md, .json)
   - Reinitialize system after adding documents

3. **Embedding Model Errors**
   - Ensure all dependencies are installed
   - Check internet connection for model download
   - Verify sufficient disk space

4. **Slow Performance**
   - Reduce document chunk size
   - Limit number of retrieved documents
   - Consider using smaller embedding model

### Debug Mode
Enable debug logging by modifying the logging level in the Python files:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Integration with Existing Systems

The RAG system is designed to integrate seamlessly with the existing AI Trader:

- Uses existing Flask web application structure
- Follows established patterns for API endpoints
- Maintains compatibility with current database systems
- Complements existing AI prediction engines

## Future Enhancements

Potential improvements for the RAG system:

1. **Multi-language Support**: Add support for documents in different languages
2. **Advanced Embedding Models**: Use domain-specific trading models
3. **Real-time Document Updates**: Automatic document updates from market data
4. **Query Caching**: Cache frequent queries for better performance
5. **Document Versioning**: Track and manage document versions
6. **Custom Embedding Models**: Train models on trading-specific data

## Security Considerations

- Document access is restricted to the web application
- No external API calls for embedding/retrieval
- Local storage of embeddings ensures data privacy
- Input validation for all API endpoints

## Support

For issues or questions about the RAG system:

1. Check the health status via `/api/rag/health`
2. Review application logs for error details
3. Verify all dependencies are properly installed
4. Ensure sufficient system resources are available
