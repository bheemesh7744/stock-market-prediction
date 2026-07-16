"""
Document Retrieval Module for AI Trader RAG System
Uses ChromaDB to retrieve relevant trading strategy documents for user queries
"""

import os
from typing import List, Dict, Any, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingDocumentRetriever:
    """Handles retrieval of relevant trading documents using ChromaDB"""
    
    def __init__(self, persist_directory: str = "./chroma_db", top_k: int = 3):
        """
        Initialize the retriever
        
        Args:
            persist_directory: Directory where ChromaDB is stored
            top_k: Number of top documents to retrieve
        """
        self.persist_directory = persist_directory
        self.top_k = top_k
        self.embeddings = self._initialize_embeddings()
        self.vector_store = None
        self._load_vector_store()
    
    def _initialize_embeddings(self) -> HuggingFaceEmbeddings:
        """Initialize HuggingFace embeddings model (same as embed.py)"""
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            logger.info("Successfully initialized HuggingFace embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {e}")
            raise
    
    def _load_vector_store(self) -> None:
        """Load existing ChromaDB vector store"""
        try:
            if os.path.exists(self.persist_directory):
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
                logger.info("Successfully loaded existing vector store")
            else:
                logger.warning(f"No vector store found at {self.persist_directory}")
                
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
    
    def retrieve_documents(self, query: str, top_k: Optional[int] = None) -> List[Document]:
        """
        Retrieve relevant documents for a given query
        
        Args:
            query: User query string
            top_k: Number of documents to retrieve (overrides default)
            
        Returns:
            List of relevant Document objects
        """
        if self.vector_store is None:
            logger.error("No vector store available. Please create embeddings first.")
            return []
        
        try:
            k = top_k if top_k is not None else self.top_k
            
            # Perform similarity search
            results = self.vector_store.similarity_search(
                query=query,
                k=k
            )
            
            logger.info(f"Retrieved {len(results)} documents for query: '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    

    
    def format_retrieved_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into context string for LLM
        
        Args:
            documents: List of retrieved Document objects
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "No relevant trading documents found."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            metadata = doc.metadata
            source = metadata.get('source', 'Unknown')
            
            context_part = f"""
Document {i} (Source: {source}):
{doc.page_content}
"""
            context_parts.append(context_part)
        
        formatted_context = "=== Relevant Trading Strategy Documents ===\n" + "\n".join(context_parts)
        return formatted_context
    
    def create_rag_prompt(self, query: str, context: str) -> str:
        """
        Create a RAG-enhanced prompt for the LLM
        
        Args:
            query: Original user query
            context: Retrieved context from documents
            
        Returns:
            Enhanced prompt with context
        """
        rag_prompt = f"""
You are an AI Trading Assistant with access to expert trading strategy documents. 
Use the provided context to answer the user's question accurately and professionally.

=== CONTEXT FROM TRADING DOCUMENTS ===
{context}

=== USER QUESTION ===
{query}

=== INSTRUCTIONS ===
1. Use the context to provide an accurate and detailed answer
2. If the context doesn't contain relevant information, say so clearly
3. Always cite the source documents when referencing specific strategies
4. Provide actionable trading advice when appropriate
5. Include risk warnings and disclaimers when discussing specific trading strategies

Please provide a comprehensive answer based on the context and your trading knowledge:
"""
        return rag_prompt
    
    def query_with_rag(self, query: str, top_k: Optional[int] = None) -> Dict[str, Any]:
        """
        Complete RAG query: retrieve documents and format for LLM
        
        Args:
            query: User query string
            top_k: Number of documents to retrieve
            
        Returns:
            Dictionary containing retrieved docs, formatted context, and RAG prompt
        """
        # Retrieve relevant documents
        documents = self.retrieve_documents(query, top_k)
        
        # Format context
        context = self.format_retrieved_context(documents)
        
        # Create RAG prompt
        rag_prompt = self.create_rag_prompt(query, context)
        
        return {
            'query': query,
            'retrieved_documents': documents,
            'context': context,
            'rag_prompt': rag_prompt,
            'num_documents': len(documents)
        }
    
    def get_document_sources(self, documents: List[Document]) -> List[str]:
        """
        Extract source information from retrieved documents
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of source filenames
        """
        sources = []
        for doc in documents:
            source = doc.metadata.get('source', 'Unknown')
            if source not in sources:
                sources.append(source)
        return sources

def main():
    """Main function to test the retrieval system"""
    # Initialize retriever
    retriever = TradingDocumentRetriever()
    
    # Test queries
    test_queries = [
        "What are the best risk management strategies?",
        "How to use RSI indicator for trading?",
        "What is momentum trading strategy?",
        "How to set stop loss orders?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        
        # Perform RAG query
        result = retriever.query_with_rag(query)
        
        print(f"Retrieved {result['num_documents']} documents")
        print(f"Sources: {retriever.get_document_sources(result['retrieved_documents'])}")
        
        # Show first 300 characters of context
        context_preview = result['context'][:300] + "..." if len(result['context']) > 300 else result['context']
        print(f"Context Preview: {context_preview}")

if __name__ == "__main__":
    main()
