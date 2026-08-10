"""
Unit test script for LightGBM integration
Run using: python test_lightgbm.py
"""
import unittest
import sys
import os
from pathlib import Path

# Add root folder to python path
sys.path.append(str(Path(__file__).parent.absolute()))

from backend.data.historical_data_manager import train_model, get_training_data
from backend.agents.deep_learning_agent import DeepLearningAgent

class TestLightGBM(unittest.TestCase):
    
    def setUp(self):
        self.symbol = "NIFTY_50"
        self.agent = DeepLearningAgent()

    def test_01_training_data(self):
        """Test that get_training_data retrieves valid dataframes"""
        data = get_training_data(self.symbol, lookback_days=50)
        self.assertNotIn("error", data)
        self.assertIn("features", data)
        self.assertGreater(len(data["features"]), 0)

    def test_02_model_training(self):
        """Test training the model for NIFTY_50"""
        res = train_model(self.symbol)
        if 'error' in res:
            self.fail(f"Model training failed: {res['error']}")
            
        self.assertIn('accuracy', res)
        self.assertIn('feature_importance', res)
        self.assertGreater(res['accuracy'], 0.0)
        
        # Verify model file was saved
        model_path = Path("data/models") / f"{self.symbol}_lightgbm.pkl"
        self.assertTrue(model_path.exists())

    def test_03_agent_inference(self):
        """Test that the agent loads and runs predictions on the model"""
        market_data = {
            'price': 24200.0,
            'open': 24150.0,
            'high': 24250.0,
            'low': 24100.0,
            'volume': 1500000
        }
        res = self.agent.generate_predictions(self.symbol, market_data)
        
        self.assertTrue(res['success'])
        self.assertEqual(res['prediction_type'], 'lightgbm')
        self.assertIn('direction', res)
        self.assertIn('confidence_score', res)
        self.assertIn('feature_importance', res)
        self.assertGreater(len(res['feature_importance']), 0)

if __name__ == '__main__':
    unittest.main()
