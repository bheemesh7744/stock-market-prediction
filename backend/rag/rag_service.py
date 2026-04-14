"""
RAG Service for AI Trader Web Application
Integrates document retrieval with the web interface to provide context-aware responses
"""

import os
import sys
from typing import Dict, Any, List
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.rag.embed import TradingDocumentEmbedder
from backend.rag.retrieve import TradingDocumentRetriever

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGService:
    """Main RAG service that integrates embedding and retrieval for the AI Trader"""
    
    def __init__(self, persist_directory: str = "./backend/rag/chroma_db"):
        """
        Initialize the RAG service
        
        Args:
            persist_directory: Directory to store/load ChromaDB
        """
        self.persist_directory = persist_directory
        self.embedder = None
        self.retriever = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize embedder and retriever services"""
        try:
            # Initialize embedder
            self.embedder = TradingDocumentEmbedder(
                persist_directory=self.persist_directory
            )
            
            # Initialize retriever
            self.retriever = TradingDocumentRetriever(
                persist_directory=self.persist_directory,
                top_k=3
            )
            
            logger.info("RAG services initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG services: {e}")
            raise
    
    def setup_knowledge_base(self, data_directory: str = None) -> bool:
        """
        Set up the knowledge base by embedding documents
        
        Args:
            data_directory: Directory containing trading documents
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if data_directory is None:
                data_directory = os.path.join(
                    os.path.dirname(__file__), "data"
                )
            
            # Load documents
            documents = self.embedder.load_documents_from_directory(data_directory)
            
            if not documents:
                logger.warning("No documents found to embed")
                return False
            
            # Create vector store
            vector_store = self.embedder.create_vector_store(documents)
            
            # Refresh retriever to use new embeddings
            self.retriever._load_vector_store()
            
            logger.info(f"Successfully set up knowledge base with {len(documents)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up knowledge base: {e}")
            return False
    
    def query_trading_assistant(self, user_query: str) -> Dict[str, Any]:
        """
        Query the trading assistant with RAG enhancement
        
        Args:
            user_query: User's trading question
            
        Returns:
            Dictionary containing response and context information
        """
        try:
            # Perform RAG query
            rag_result = self.retriever.query_with_rag(user_query)
            
            # Extract relevant information
            response = {
                'user_query': user_query,
                'context': rag_result['context'],
                'rag_prompt': rag_result['rag_prompt'],
                'sources': self.retriever.get_document_sources(rag_result['retrieved_documents']),
                'num_documents': rag_result['num_documents'],
                'success': True
            }
            
            logger.info(f"Successfully processed query: '{user_query}' with {rag_result['num_documents']} documents")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'user_query': user_query,
                'error': str(e),
                'success': False,
                'context': 'Unable to retrieve relevant documents.',
                'sources': [],
                'num_documents': 0
            }
    
    def get_available_documents(self) -> List[str]:
        """
        Get list of available document sources
        
        Returns:
            List of document filenames
        """
        try:
            data_directory = os.path.join(os.path.dirname(__file__), "data")
            if os.path.exists(data_directory):
                documents = [f for f in os.listdir(data_directory) 
                           if f.endswith(('.txt', '.md', '.json'))]
                return documents
            return []
        except Exception as e:
            logger.error(f"Error getting available documents: {e}")
            return []
    
    def add_new_document(self, file_path: str, content: str = None) -> bool:
        """
        Add a new document to the knowledge base
        
        Args:
            file_path: Path to the document file
            content: Document content (if not reading from file)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from langchain.schema import Document
            
            if content is None:
                # Read content from file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # Create document with metadata
            filename = os.path.basename(file_path)
            metadata = {
                'source': filename,
                'file_type': filename.split('.')[-1],
                'file_path': file_path
            }
            
            document = Document(page_content=content, metadata=metadata)
            
            # Add to vector store
            self.embedder.add_documents([document])
            
            # Refresh retriever
            self.retriever._load_vector_store()
            
            logger.info(f"Successfully added document: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check the health status of the RAG system
        
        Returns:
            Dictionary containing health status information
        """
        try:
            # Check if vector store exists
            vector_store_exists = os.path.exists(self.persist_directory)
            
            # Check if data directory has documents
            data_dir = os.path.join(os.path.dirname(__file__), "data")
            data_dir_exists = os.path.exists(data_dir)
            document_count = len([f for f in os.listdir(data_dir) 
                                if f.endswith(('.txt', '.md', '.json'))]) if data_dir_exists else 0
            
            # Test retrieval functionality
            test_query = "trading strategy"
            test_result = self.retriever.retrieve_documents(test_query, top_k=1)
            retrieval_working = len(test_result) > 0
            
            health_status = {
                'status': 'healthy' if all([vector_store_exists, retrieval_working]) else 'unhealthy',
                'vector_store_exists': vector_store_exists,
                'data_directory_exists': data_dir_exists,
                'document_count': document_count,
                'retrieval_working': retrieval_working,
                'embedder_initialized': self.embedder is not None,
                'retriever_initialized': self.retriever is not None
            }
            
            return health_status
            
        except Exception as e:
            logger.error(f"Error during health check: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }

# Global RAG service instance
rag_service = None

def get_rag_service() -> RAGService:
    """Get or create the global RAG service instance"""
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service

def initialize_rag_system() -> bool:
    """
    Initialize the RAG system with default documents
    
    Returns:
        True if successful, False otherwise
    """
    try:
        service = get_rag_service()
        
        # Check if knowledge base needs setup
        health = service.health_check()
        
        if not health['vector_store_exists'] or health['document_count'] == 0:
            logger.info("Setting up knowledge base...")
            success = service.setup_knowledge_base()
            if success:
                logger.info("RAG system initialized successfully")
            else:
                logger.error("Failed to set up knowledge base")
            return success
        else:
            logger.info("RAG system already initialized")
            return True
            
    except Exception as e:
        logger.error(f"Error initializing RAG system: {e}")
        return False

# Example usage and testing
if __name__ == "__main__":
    # Initialize the RAG system
    print("Initializing RAG system...")
    success = initialize_rag_system()
    
    if success:
        print("RAG system initialized successfully!")
        
        # Get the service
        service = get_rag_service()
        
        # Test queries
        test_queries = [
            "What are the best risk management strategies?",
            "How do I use RSI indicator for trading?",
            "What is momentum trading?",
            "How should I handle market psychology?"
        ]
        
        for query in test_queries:
            print(f"\n{'='*50}")
            print(f"Query: {query}")
            print(f"{'='*50}")
            
            result = service.query_trading_assistant(query)
            
            if result['success']:
                print(f"Retrieved {result['num_documents']} documents")
                print(f"Sources: {result['sources']}")
                print(f"Context Preview: {result['context'][:200]}...")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Health check
        print(f"\n{'='*50}")
        print("Health Check:")
        print(f"{'='*50}")
        health = service.health_check()
        for key, value in health.items():
            print(f"{key}: {value}")
    
    else:
        print("Failed to initialize RAG system")
