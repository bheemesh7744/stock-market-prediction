"""
RAG Pipeline - Unified Question Processing
Routes all user questions through the RAG system before LLM processing
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .rag_service import get_rag_service, initialize_rag_system
from .llm_integration import get_llm_instance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGPipeline:
    """Unified RAG pipeline for processing all user questions"""
    
    def __init__(self):
        """Initialize the RAG pipeline"""
        self.rag_service = None
        self.llm_integration = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize RAG and LLM components"""
        try:
            # Initialize RAG service
            self.rag_service = get_rag_service()
            
            # Initialize LLM integration
            self.llm_integration = get_llm_instance()
            
            logger.info("RAG Pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RAG Pipeline: {e}")
            # Don't raise error - allow graceful degradation
    
    def process_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a user question through the complete RAG pipeline
        
        Args:
            question: User's question
            context: Additional context (optional)
            
        Returns:
            Dictionary containing the response and metadata
        """
        start_time = datetime.now()
        
        try:
            # Step 1: Retrieve relevant documents using RAG
            rag_result = self._retrieve_context(question)
            
            # Step 2: Create RAG-enhanced prompt
            enhanced_prompt = self._create_enhanced_prompt(question, rag_result, context)
            
            # Step 3: Generate response using LLM
            llm_result = self._generate_llm_response(enhanced_prompt)
            
            # Step 4: Compile final response
            final_response = self._compile_response(
                question=question,
                rag_result=rag_result,
                llm_result=llm_result,
                processing_time=(datetime.now() - start_time).total_seconds()
            )
            
            logger.info(f"Successfully processed question: '{question[:50]}...'")
            return final_response
            
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return self._create_error_response(question, str(e), start_time)
    
    def _retrieve_context(self, question: str) -> Dict[str, Any]:
        """
        Retrieve relevant context using RAG system
        
        Args:
            question: User's question
            
        Returns:
            RAG retrieval result
        """
        try:
            if self.rag_service is None:
                return {
                    'success': False,
                    'error': 'RAG service not available',
                    'context': 'Unable to retrieve trading documents.',
                    'sources': [],
                    'num_documents': 0
                }
            
            # Query the RAG service
            rag_result = self.rag_service.query_trading_assistant(question)
            
            return rag_result
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return {
                'success': False,
                'error': str(e),
                'context': 'Error retrieving trading documents.',
                'sources': [],
                'num_documents': 0
            }
    
    def _create_enhanced_prompt(self, question: str, rag_result: Dict[str, Any], 
                              additional_context: Optional[Dict[str, Any]] = None) -> str:
        """
        Create an enhanced prompt with RAG context
        
        Args:
            question: User's question
            rag_result: Result from RAG retrieval
            additional_context: Any additional context
            
        Returns:
            Enhanced prompt for LLM
        """
        base_prompt = f"""You are an expert AI Trading Assistant with access to comprehensive trading strategy documents. 

USER QUESTION: {question}

RETRIEVED TRADING DOCUMENTS:
{rag_result.get('context', 'No specific documents found.')}

SOURCES: {', '.join(rag_result.get('sources', []))}

ADDITIONAL CONTEXT:
{json.dumps(additional_context, indent=2) if additional_context else 'None'}

INSTRUCTIONS:
1. Use the retrieved trading documents to provide an accurate and detailed answer
2. If the documents don't contain relevant information, clearly state that
3. Always cite the source documents when referencing specific strategies
4. Provide actionable trading advice when appropriate
5. Include risk warnings and disclaimers for trading strategies
6. Structure your response with clear headings and bullet points
7. Be professional, educational, and helpful

Please provide a comprehensive answer based on the retrieved context and your trading expertise:"""
        
        return base_prompt
    
    def _generate_llm_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate LLM response
        
        Args:
            prompt: Enhanced prompt with RAG context
            
        Returns:
            LLM generation result
        """
        try:
            if self.llm_integration is None:
                return {
                    'success': False,
                    'error': 'LLM service not available',
                    'response': 'LLM service is unavailable. Please try again later.',
                    'model': None,
                    'tokens_used': None
                }
            
            # Generate response
            llm_result = self.llm_integration.generate_response(prompt)
            
            return llm_result
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': 'Error generating response. Please try again.',
                'model': None,
                'tokens_used': None
            }
    
    def _compile_response(self, question: str, rag_result: Dict[str, Any], 
                         llm_result: Dict[str, Any], processing_time: float) -> Dict[str, Any]:
        """
        Compile the final response with all metadata
        
        Args:
            question: Original question
            rag_result: RAG retrieval result
            llm_result: LLM generation result
            processing_time: Total processing time
            
        Returns:
            Complete response dictionary
        """
        return {
            'success': True,
            'question': question,
            'answer': llm_result.get('response', llm_result.get('fallback_response', 'No response generated.')),
            'sources': rag_result.get('sources', []),
            'context_used': rag_result.get('context', '')[:500] + '...' if len(rag_result.get('context', '')) > 500 else rag_result.get('context', ''),
            'num_documents_retrieved': rag_result.get('num_documents', 0),
            'llm_model': llm_result.get('model', 'unknown'),
            'tokens_used': llm_result.get('tokens_used'),
            'rag_success': rag_result.get('success', False),
            'llm_success': llm_result.get('success', False),
            'processing_time_seconds': round(processing_time, 2),
            'timestamp': datetime.now().isoformat(),
            'pipeline_version': '1.0'
        }
    
    def _create_error_response(self, question: str, error: str, start_time: datetime) -> Dict[str, Any]:
        """
        Create error response
        
        Args:
            question: Original question
            error: Error message
            start_time: Processing start time
            
        Returns:
            Error response dictionary
        """
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'success': False,
            'question': question,
            'answer': f"I'm sorry, I encountered an error while processing your question: {error}. Please try again or contact support if the issue persists.",
            'sources': [],
            'context_used': '',
            'num_documents_retrieved': 0,
            'llm_model': None,
            'tokens_used': None,
            'rag_success': False,
            'llm_success': False,
            'processing_time_seconds': round(processing_time, 2),
            'timestamp': datetime.now().isoformat(),
            'error': error,
            'pipeline_version': '1.0'
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check the health of the entire RAG pipeline
        
        Returns:
            Health status dictionary
        """
        health = {
            'pipeline_status': 'unknown',
            'rag_service': False,
            'llm_service': False,
            'overall_status': 'unhealthy',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Check RAG service
            if self.rag_service:
                rag_health = self.rag_service.health_check()
                health['rag_service'] = rag_health.get('status') == 'healthy'
            else:
                health['rag_service'] = False
            
            # Check LLM service
            if self.llm_integration:
                health['llm_service'] = True  # LLM service is always available (has fallback)
            else:
                health['llm_service'] = False
            
            # Determine overall status
            if health['rag_service'] and health['llm_service']:
                health['overall_status'] = 'healthy'
                health['pipeline_status'] = 'operational'
            elif health['llm_service']:
                health['overall_status'] = 'degraded'
                health['pipeline_status'] = 'limited (RAG unavailable)'
            else:
                health['overall_status'] = 'unhealthy'
                health['pipeline_status'] = 'offline'
                
        except Exception as e:
            health['error'] = str(e)
            health['overall_status'] = 'error'
        
        return health
    
    def initialize_system(self) -> bool:
        """
        Initialize the RAG system
        
        Returns:
            True if successful, False otherwise
        """
        try:
            success = initialize_rag_system()
            if success:
                logger.info("RAG Pipeline system initialized successfully")
            else:
                logger.warning("RAG Pipeline initialization failed")
            return success
        except Exception as e:
            logger.error(f"Error initializing RAG Pipeline system: {e}")
            return False

# Global pipeline instance
rag_pipeline = None

def get_rag_pipeline() -> RAGPipeline:
    """Get or create the global RAG pipeline instance"""
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline

def process_trading_question(question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to process a trading question
    
    Args:
        question: User's trading question
        context: Additional context (optional)
        
    Returns:
        Response dictionary
    """
    pipeline = get_rag_pipeline()
    return pipeline.process_question(question, context)

# Import json for the prompt creation
import json
