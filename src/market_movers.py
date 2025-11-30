"""Display most active stocks and market movers."""

import sys
import logging
from market_data import MarketDataFetcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def display_market_movers():
    """Display current market movers and active stocks from StockTwits."""
    print("=" * 100)
    print("STOCKTWITS - MOST ACTIVE EQUITIES")
    print("=" * 100)
    
    fetcher = MarketDataFetcher()
    
    try:
        # Most Active Stocks
        print("\n[1] TOP 10 MOST ACTIVE EQUITIES (BY TRADING VOLUME)")
        print("-" * 100)
        active_stocks = fetcher.get_most_active_stocks(limit=10)
        
        if active_stocks:
            print(f"{'Rank':<6} {'Symbol':<8} {'Company Name':<25} {'Price':<12} {'% Change':<12} {'Volume':<15}")
            print("-" * 100)
            for idx, stock in enumerate(active_stocks, 1):
                symbol = stock.get('symbol', 'N/A')
                name = stock.get('name', 'N/A')
                price = stock.get('price', 0)
                change = stock.get('change', 'N/A')
                volume = stock.get('volume', 'N/A')
                
                # Color code for positive/negative
                if isinstance(price, (int, float)):
                    print(f"{idx:<6} {symbol:<8} {name:<25} ${price:<11.2f} {change:<12} {volume:<15}")
                else:
                    print(f"{idx:<6} {symbol:<8} {name:<25} {price:<12} {change:<12} {volume:<15}")
        
        # Top Gainers
        print("\n[2] TOP 5 GAINERS (HIGHEST % GAIN)")
        print("-" * 100)
        gainers = fetcher.get_gainers(limit=5)
        
        if gainers:
            print(f"{'Rank':<6} {'Symbol':<8} {'Company Name':<25} {'Price':<12} {'% Change':<12} {'Volume':<15}")
            print("-" * 100)
            for idx, stock in enumerate(gainers, 1):
                symbol = stock.get('symbol', 'N/A')
                name = stock.get('name', 'N/A')
                price = stock.get('price', 0)
                change = stock.get('change', 'N/A')
                volume = stock.get('volume', 'N/A')
                
                if isinstance(price, (int, float)) and price > 0:
                    print(f"{idx:<6} {symbol:<8} {name:<25} ${price:<11.2f} {change:<12} {volume:<15}")
                else:
                    print(f"{idx:<6} {symbol:<8} {name:<25} {price:<12} {change:<12} {volume:<15}")
        
        # Top Losers
        print("\n[3] TOP 5 LOSERS (HIGHEST % LOSS)")
        print("-" * 100)
        losers = fetcher.get_losers(limit=5)
        
        if losers:
            print(f"{'Rank':<6} {'Symbol':<8} {'Company Name':<25} {'Price':<12} {'% Change':<12} {'Volume':<15}")
            print("-" * 100)
            for idx, stock in enumerate(losers, 1):
                symbol = stock.get('symbol', 'N/A')
                name = stock.get('name', 'N/A')
                price = stock.get('price', 0)
                change = stock.get('change', 'N/A')
                volume = stock.get('volume', 'N/A')
                
                if isinstance(price, (int, float)) and price > 0:
                    print(f"{idx:<6} {symbol:<8} {name:<25} ${price:<11.2f} {change:<12} {volume:<15}")
                else:
                    print(f"{idx:<6} {symbol:<8} {name:<25} {price:<12} {change:<12} {volume:<15}")
        
        # Summary Statistics
        print("\n[4] MARKET SUMMARY")
        print("-" * 100)
        
        if active_stocks:
            total_volume = 0
            total_price = 0
            count = 0
            
            for stock in active_stocks:
                volume = stock.get('volume', '0M')
                if isinstance(volume, str) and 'M' in volume:
                    try:
                        total_volume += float(volume.replace('M', ''))
                    except:
                        pass
                
                price = stock.get('price', 0)
                if isinstance(price, (int, float)) and price > 0:
                    total_price += price
                    count += 1
            
            avg_price = total_price / count if count > 0 else 0
            
            print(f"  Total Active Volume (Top 10): {total_volume:.2f}M shares")
            print(f"  Average Stock Price (Top 10): ${avg_price:.2f}")
            
            if gainers:
                print(f"  Top Gainer: {gainers[0]['symbol']} ({gainers[0]['change']})")
            if losers:
                print(f"  Top Loser:  {losers[0]['symbol']} ({losers[0]['change']})")
        
        print("\n" + "=" * 100)
        print("✓ StockTwits Market Data Display Complete")
        print("=" * 100)
        print("\nSource: StockTwits Sentiment/Most-Active Dashboard")
        print("URL: https://stocktwits.com/sentiment/most-active")
        print("=" * 100)
        
    except Exception as e:
        logger.error(f"Error displaying market movers: {e}")
        print(f"Error: {e}")
    finally:
        fetcher.close()


if __name__ == "__main__":
    display_market_movers()
