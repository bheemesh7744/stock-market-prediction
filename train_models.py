"""
Train LightGBM Models - Command line tool to train models for Indian Market indices.
Run this using: python train_models.py
"""
import argparse
import sys
import logging
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("train_models")

# Add parent directory to path to support imports
sys.path.append(str(Path(__file__).parent.absolute()))

from backend.data.historical_data_manager import train_model, collect_historical_data

def main():
    parser = argparse.ArgumentParser(description="Train LightGBM models for Agentic AI Trader")
    parser.add_argument("--symbols", type=str, default="NIFTY_50,BANK_NIFTY,SENSEX", 
                        help="Comma-separated symbols to train (default: NIFTY_50,BANK_NIFTY,SENSEX)")
    parser.add_argument("--collect-first", action="store_true", default=True,
                        help="Collect/download latest historical data before training (default: True)")
    
    args = parser.parse_args()
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    
    logger.info(f"Target symbols for training: {symbols}")
    
    for symbol in symbols:
        print(f"\n==================================================")
        print(f" TRAINING MODEL FOR: {symbol} ")
        print(f"==================================================")
        
        if args.collect_first:
            logger.info(f"Downloading latest historical data for {symbol}...")
            collect_res = collect_historical_data(symbol, years=5)
            if 'error' in collect_res:
                logger.error(f"Failed to collect historical data: {collect_res['error']}")
                print(f"Skipping training due to data collection failure.")
                continue
            logger.info(f"Data collected: {collect_res.get('data_points', 0)} daily bars")
            
        logger.info(f"Running model training for {symbol}...")
        result = train_model(symbol)
        
        if 'error' in result:
            print(f"❌ ERROR training model: {result['error']}")
        else:
            print(f"✅ SUCCESS training model!")
            print(f"   Accuracy:  {result.get('accuracy') * 100:.2f}%")
            print(f"   Precision: {result.get('precision') * 100:.2f}%")
            print(f"   Recall:    {result.get('recall') * 100:.2f}%")
            print(f"   Data size: {result.get('data_points')} points")
            print(f"   Trained at: {result.get('trained_at')}")

if __name__ == "__main__":
    main()
