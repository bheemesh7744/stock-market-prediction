"""
Document Embedding Module for AI Trader RAG System
Uses LangChain and sentence-transformers to create embeddings from trading strategy documents
"""

import os
import json
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingDocumentEmbedder:
    """Handles embedding of trading strategy documents using LangChain"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize the embedder with ChromaDB persistence
        
        Args:
            persist_directory: Directory to store ChromaDB embeddings
        """
        self.persist_directory = persist_directory
        self.embeddings = self._initialize_embeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store = None
        
    def _initialize_embeddings(self) -> HuggingFaceEmbeddings:
        """Initialize HuggingFace embeddings model"""
        try:
            # Using a lightweight but effective model for trading documents
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
    
    def load_documents_from_directory(self, directory_path: str) -> List[Document]:
        """
        Load trading strategy documents from a directory
        
        Args:
            directory_path: Path to directory containing trading documents
            
        Returns:
            List of LangChain Document objects
        """
        documents = []
        
        if not os.path.exists(directory_path):
            logger.error(f"Directory {directory_path} does not exist")
            return documents
            
        for filename in os.listdir(directory_path):
            if filename.endswith(('.txt', '.md', '.json')):
                file_path = os.path.join(directory_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Create metadata for the document
                    metadata = {
                        'source': filename,
                        'file_type': filename.split('.')[-1],
                        'file_path': file_path
                    }
                    
                    # Create Document object
                    doc = Document(page_content=content, metadata=metadata)
                    documents.append(doc)
                    
                    logger.info(f"Loaded document: {filename}")
                    
                except Exception as e:
                    logger.error(f"Error loading file {filename}: {e}")
                    
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks for better embedding
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of chunked Document objects
        """
        try:
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error splitting documents: {e}")
            return documents
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """
        Create and populate ChromaDB vector store with document embeddings
        
        Args:
            documents: List of Document objects to embed
            
        Returns:
            ChromaDB vector store
        """
        try:
            # Split documents into chunks
            chunks = self.split_documents(documents)
            
            # Create ChromaDB vector store
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            # Persist the vector store
            self.vector_store.persist()
            
            logger.info(f"Successfully created vector store with {len(chunks)} document chunks")
            return self.vector_store
            
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def load_existing_vector_store(self) -> Chroma:
        """
        Load existing ChromaDB vector store from disk
        
        Returns:
            ChromaDB vector store
        """
        try:
            if os.path.exists(self.persist_directory):
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
                logger.info("Successfully loaded existing vector store")
                return self.vector_store
            else:
                logger.warning(f"No existing vector store found at {self.persist_directory}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return None
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add new documents to existing vector store
        
        Args:
            documents: List of Document objects to add
        """
        try:
            if self.vector_store is None:
                self.load_existing_vector_store()
                
            if self.vector_store is None:
                logger.error("No vector store available. Create one first.")
                return
                
            chunks = self.split_documents(documents)
            self.vector_store.add_documents(chunks)
            self.vector_store.persist()
            
            logger.info(f"Added {len(chunks)} document chunks to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")

def main():
    """Main function to test the embedding system"""
    # Initialize embedder
    embedder = TradingDocumentEmbedder()
    
    # Load documents from data directory
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    documents = embedder.load_documents_from_directory(data_dir)
    
    if not documents:
        print("No documents found to embed")
        return
    
    # Create vector store
    vector_store = embedder.create_vector_store(documents)
    
    print(f"Successfully embedded {len(documents)} documents")
    print(f"Vector store persisted at: {embedder.persist_directory}")

if __name__ == "__main__":
    main()
