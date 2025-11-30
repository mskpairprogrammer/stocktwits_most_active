"""Extract active stocks and save to file."""

import sys
import os
import logging
import subprocess
from datetime import datetime
from market_data import MarketDataFetcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_and_save_stocks(output_file: str) -> bool:
    """Extract active stocks and save to file.
    
    Args:
        output_file: Path to save the stock data
        
    Returns:
        True if successful, False otherwise
    """
    try:
        fetcher = MarketDataFetcher()
        
        # Get active stocks
        active_stocks = fetcher.get_most_active_stocks(limit=10)
        gainers = fetcher.get_gainers(limit=5)
        losers = fetcher.get_losers(limit=5)
        
        if not active_stocks:
            logger.error("No active stocks found")
            return False
        
        # Prepare content - Only symbols
        content = []
        
        for stock in active_stocks:
            symbol = stock.get('symbol', 'N/A')
            content.append(symbol)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        logger.info(f"Successfully saved active stocks to {output_file}")
        print(f"✓ Active stocks extracted and saved to: {output_file}")
        print(f"✓ Total records: {len(active_stocks)} most active + {len(gainers)} gainers + {len(losers)} losers")
        
        # Trigger DesktopAuto.exe
        desktop_auto_path = r"C:\Users\senth\OneDrive\Documents\desktop_auto\dist\DesktopAuto.exe"
        desktop_auto_dir = r"C:\Users\senth\OneDrive\Documents\desktop_auto\dist"
        if os.path.exists(desktop_auto_path):
            try:
                logger.info(f"Triggering {desktop_auto_path}...")
                # Launch with proper working directory so it can find config files
                subprocess.Popen(
                    [desktop_auto_path],
                    cwd=desktop_auto_dir,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                print("✓ DesktopAuto.exe triggered")
            except Exception as e:
                logger.error(f"Failed to trigger DesktopAuto.exe: {e}")
                print(f"✗ Failed to trigger automation: {e}")
        else:
            logger.warning(f"DesktopAuto.exe not found at {desktop_auto_path}")
            print(f"✗ DesktopAuto.exe not found at {desktop_auto_path}")
        
        fetcher.close()
        return True
        
    except Exception as e:
        logger.error(f"Error extracting stocks: {e}", exc_info=True)
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    output_path = r"C:\Users\senth\OneDrive\Documents\data\screenshots\stock_symbols.txt"
    success = extract_and_save_stocks(output_path)
    sys.exit(0 if success else 1)
