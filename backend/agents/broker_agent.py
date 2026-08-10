import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Try to import dhanhq, but don't fail if not installed yet
try:
    from dhanhq import dhanhq
    DHAN_SDK_AVAILABLE = True
except ImportError:
    DHAN_SDK_AVAILABLE = False
    logger.warning("dhanhq SDK not found. Install it with: pip install dhanhq")

class BrokerAgent:
    """
    Agent responsible for interacting with the Stock Broker API (DhanHQ).
    Handles order execution, portfolio fetching, and position management.
    """
    
    def __init__(self):
        self.client_id = os.environ.get('DHAN_CLIENT_ID', '')
        self.access_token = os.environ.get('DHAN_ACCESS_TOKEN', '')
        self.live_trading_enabled = os.environ.get('ENABLE_LIVE_TRADING', 'False').lower() in ('true', '1', 'yes')
        self.dhan = None
        self.connected = False
        
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize the Dhan API Client"""
        if not DHAN_SDK_AVAILABLE:
            logger.error("Cannot initialize Dhan client: dhanhq SDK not available.")
            return
            
        if not self.client_id or not self.access_token:
            logger.warning("Dhan API credentials not found in environment variables.")
            return
            
        try:
            self.dhan = dhanhq(
                client_id=self.client_id,
                access_token=self.access_token
            )
            # Test connection by getting funds
            funds = self.dhan.get_fund_limits()
            if funds and 'data' in funds:
                self.connected = True
                logger.info("Successfully connected to DhanHQ Broker API.")
            else:
                logger.error(f"Failed to connect to DhanHQ. Response: {funds}")
        except Exception as e:
            logger.error(f"Error initializing Dhan client: {e}")
            
    def is_ready(self) -> bool:
        """Check if the broker agent is ready for live trading"""
        return self.connected and self.live_trading_enabled
        
    def place_order(self, symbol: str, side: str, quantity: int = 1, product_type: str = 'INTRADAY', price: float = 0.0) -> Dict[str, Any]:
        """
        Place an order to the exchange.
        If live_trading is disabled, performs a mock paper trade.
        """
        side_upper = side.upper()
        if side_upper not in ['BUY', 'SELL']:
            return {'success': False, 'message': f'Invalid side: {side}', 'order_id': None}
            
        # Determine exchange segment
        exchange_segment = self.dhan.NSE if self.connected else 'NSE'
        if "SENSEX" in symbol:
            exchange_segment = self.dhan.BSE if self.connected else 'BSE'
            
        # MOCK MODE (Paper Trading)
        if not self.is_ready():
            logger.info(f"[MOCK TRADE] Would execute: {side_upper} {quantity}x {symbol} @ {price if price > 0 else 'MARKET'}")
            return {
                'success': True, 
                'message': 'Mock trade executed successfully (Live trading disabled or credentials missing)',
                'order_id': f'MOCK_{os.urandom(4).hex().upper()}',
                'mode': 'paper'
            }
            
        # LIVE MODE
        try:
            # Prepare transaction type
            transaction_type = self.dhan.BUY if side_upper == 'BUY' else self.dhan.SELL
            
            # Prepare order type
            order_type = self.dhan.LIMIT if price > 0 else self.dhan.MARKET
            
            # Prepare product type (INTRADAY or CNC/MARGIN)
            prod_type = self.dhan.INTRA if product_type.upper() == 'INTRADAY' else self.dhan.CNC
            
            logger.info(f"Placing LIVE order on Dhan: {transaction_type} {quantity} {symbol} at {order_type}")
            
            # Place the actual order
            # Note: security_id requires looking up the exact token from Dhan's master list. 
            # We use a placeholder here for the structural integration.
            response = self.dhan.place_order(
                security_id='1333', # Placeholder - requires scrip master integration
                exchange_segment=exchange_segment,
                transaction_type=transaction_type,
                quantity=quantity,
                order_type=order_type,
                product_type=prod_type,
                price=price
            )
            
            if response and response.get('status') == 'success':
                order_id = response.get('data', {}).get('orderId')
                logger.info(f"Order placed successfully. Order ID: {order_id}")
                return {
                    'success': True,
                    'message': 'Order placed successfully',
                    'order_id': order_id,
                    'mode': 'live',
                    'response': response.get('data')
                }
            else:
                error_msg = response.get('remarks', 'Unknown error') if response else 'Empty response'
                logger.error(f"Order failed: {error_msg}")
                return {
                    'success': False,
                    'message': f"Broker rejected order: {error_msg}",
                    'order_id': None,
                    'mode': 'live'
                }
                
        except Exception as e:
            logger.error(f"Exception during order placement: {e}")
            return {
                'success': False,
                'message': f"System error placing order: {str(e)}",
                'order_id': None,
                'mode': 'live'
            }
            
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Fetch status of a specific order"""
        if not self.is_ready():
            return {'status': 'COMPLETED (Mock)'}
            
        try:
            status = self.dhan.get_order_by_id(order_id)
            return status
        except Exception as e:
            logger.error(f"Error fetching order {order_id}: {e}")
            return {'error': str(e)}

# Global instance
broker_agent = BrokerAgent()
