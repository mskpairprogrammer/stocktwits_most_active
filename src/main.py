"""Main entry point for the StockTwits analyzer - Fetch active stocks and trigger automation."""

import sys
import logging
from market_data import MarketDataFetcher
from export_stocks import extract_and_save_stocks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Placeholder - no longer used
SAMPLE_POSTS = [
    "SMX Stock Surged Over 220% Today – Check out this molecular technology play!",
    "Nio Gets A Price Target Hike from Freedom Capital, analyst expects revenue at new record levels",
    "Goldman Sachs identifies 6 stocks that are favorites of mutual funds and hedge funds",
    "Trading SPY today, keeping eyes on DIA and QQQ for market direction",
    "NAIL stock looking strong this week, DX and BHE also moving",
    "BOB.X is trending hard right now, TMDX and CRDO gaining momentum",
    "ALGO.X and MOS are my top picks for tomorrow",
    "AAPL showing bullish signals, MSFT consolidating",
    "GOOGL breaking out, tech sector leading the market",
    "Tesla TSLA and Nvidia NVDA continue to dominate",
    "SPY breaks through resistance, bulls in control",
    "Market rotation: DIA outperforming, tech weakness with SPY and QQQ",
    "NAIL and DX experiencing volatility today",
    "Emerging plays: SMX, NIO, and TMDX worth watching",
    "$AAPL $MSFT $GOOGL these mega caps driving overall sentiment",
    "Bearish on QQQ this week, watching SPY support",
    "Gold miners CRDO and energy stocks like MOS on watch list",
    "DIA at all-time highs, sector rotation favorites among fund managers",
    "Small cap plays: ALGO.X and BHE show potential",
]


# Phase 3 & 4 logic only - Market Data & Automation
def main():
    """Main application flow: Fetch market data and export symbols."""
    print("=" * 80)
    print("StockTwits Most Active Equities Analyzer")
    print("=" * 80)
    
    fetcher = MarketDataFetcher()
    
    try:
        # Phase 3: Fetch Most Active Equities
        print("\n[Phase 3] Fetching Most Active Equities...")
        print("-" * 80)
        
        active_stocks = fetcher.get_most_active_stocks(limit=10)
        gainers = fetcher.get_gainers(limit=5)
        losers = fetcher.get_losers(limit=5)
        
        if not active_stocks:
            print("✗ No active stocks found")
            return False
        
        print(f"✓ Found {len(active_stocks)} most active equities")
        print(f"✓ Top Gainer: {gainers[0]['symbol']} ({gainers[0]['change']})" if gainers else "")
        print(f"✓ Top Loser: {losers[0]['symbol']} ({losers[0]['change']})" if losers else "")
        
        # Display the data
        print("\n[Most Active Equities - Top 10]")
        print("-" * 80)
        print(f"{'Rank':<6} {'Symbol':<8} {'Company':<25} {'Price':<12} {'% Change':<12} {'Volume':<15}")
        print("-" * 80)
        
        for idx, stock in enumerate(active_stocks, 1):
            symbol = stock.get('symbol', 'N/A')
            name = stock.get('name', 'N/A')
            price = stock.get('price', 0)
            change = stock.get('change', 'N/A')
            volume = stock.get('volume', 'N/A')
            
            if isinstance(price, (int, float)):
                print(f"{idx:<6} {symbol:<8} {name:<25} ${price:<11.2f} {change:<12} {volume:<15}")
        
        # Phase 4: Export & Automation
        print("\n[Phase 4] Export Symbols & Trigger Automation...")
        print("-" * 80)
        
        output_path = r"C:\Users\senth\OneDrive\Documents\data\screenshots\stock_symbols.txt"
        success = extract_and_save_stocks(output_path)
        
        if success:
            print("\n✓ Workflow Complete!")
            print("  - Symbols exported to file")
            print("  - DesktopAuto.exe triggered for chart analysis")
        
        print("\n" + "=" * 80)
        
        fetcher.close()
        return success
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
