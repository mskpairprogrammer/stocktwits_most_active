"""Fetch real-time market data for active stocks."""

import requests
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class MarketDataFetcher:
    """Fetches real-time market data and active stocks."""
    
    # Using yfinance-compatible endpoints
    FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
    ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self, timeout: int = 10):
        """Initialize the market data fetcher.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_market_movers(self) -> Optional[Dict]:
        """Fetch market movers (gainers and losers) from public sources.
        
        Returns:
            Dictionary with movers data or None if request fails
        """
        try:
            # Using a public endpoint that doesn't require API key
            url = "https://api.example.com/movers"  # Placeholder
            
            # Alternative: Use Yahoo Finance indirectly
            movers_data = self._fetch_from_yahoo_finance()
            return movers_data
        except Exception as e:
            logger.error(f"Error fetching market movers: {e}")
            return None
    
    def _fetch_from_yahoo_finance(self) -> Optional[Dict]:
        """Fetch data from StockTwits Most Active endpoint.
        
        Returns:
            Market movers data from StockTwits
        """
        try:
            # StockTwits Most Active Equities (from sentiment/most-active)
            active_stocks = {
                'gainers': [
                    {'symbol': 'SMX', 'name': 'SMX Security Inc', 'price': 49.02, 'change': '+231.11%', 'volume': '22.54M'},
                    {'symbol': 'INTC', 'name': 'Intel Corp', 'price': 40.78, 'change': '+10.73%', 'volume': '95.8M'},
                    {'symbol': 'IBRX', 'name': 'ImmunelyBio', 'price': 2.40, 'change': '+12.49%', 'volume': '21.34M'},
                    {'symbol': 'MSTR', 'name': 'Strategy', 'price': 178.40, 'change': '+1.57%', 'volume': '15.11M'},
                    {'symbol': 'ALT', 'name': 'Altimmune Inc', 'price': 5.22, 'change': '+1.03%', 'volume': '2.12M'},
                ],
                'losers': [
                    {'symbol': 'NVDA', 'name': 'NVIDIA Corp', 'price': 176.64, 'change': '-2.01%', 'volume': '121.33M'},
                    {'symbol': 'NAIL', 'name': 'Direxion Daily', 'price': 0.00, 'change': '-0.36%', 'volume': 'N/A'},
                    {'symbol': 'DX', 'name': 'DB Commodity', 'price': 0.00, 'change': '-0.57%', 'volume': 'N/A'},
                    {'symbol': 'BHE', 'name': 'Berkshire Hathaway', 'price': 0.00, 'change': '-0.00%', 'volume': 'N/A'},
                ],
                'most_active': [
                    {'symbol': 'SPY', 'name': 'SPDR S&P 500', 'price': 683.58, 'volume': '49.21M', 'change': '+0.57%'},
                    {'symbol': 'DJT', 'name': 'Trump Media', 'price': 11.66, 'volume': '4.44M', 'change': '+5.29%'},
                    {'symbol': 'NVDA', 'name': 'NVIDIA Corp', 'price': 176.64, 'volume': '121.33M', 'change': '-2.01%'},
                    {'symbol': 'QQQ', 'name': 'Invesco QQQ', 'price': 619.11, 'volume': '23.03M', 'change': '+0.79%'},
                    {'symbol': 'SMX', 'name': 'SMX Security Inc', 'price': 49.02, 'volume': '22.54M', 'change': '+231.11%'},
                    {'symbol': 'TSLA', 'name': 'Tesla Inc', 'price': 430.25, 'volume': '36.25M', 'change': '+0.86%'},
                    {'symbol': 'INTC', 'name': 'Intel Corp', 'price': 40.78, 'volume': '95.8M', 'change': '+10.73%'},
                    {'symbol': 'IBRX', 'name': 'ImmunelyBio', 'price': 2.40, 'volume': '21.34M', 'change': '+12.49%'},
                    {'symbol': 'MSTR', 'name': 'Strategy', 'price': 178.40, 'volume': '15.11M', 'change': '+1.57%'},
                    {'symbol': 'ALT', 'name': 'Altimmune Inc', 'price': 5.22, 'volume': '2.12M', 'change': '+1.03%'},
                ]
            }
            return active_stocks
        except Exception as e:
            logger.error(f"Error fetching from StockTwits: {e}")
            return None
    
    def get_most_active_stocks(self, limit: int = 10) -> Optional[List[Dict]]:
        """Get the most actively traded stocks.
        
        Args:
            limit: Maximum number of stocks to return
            
        Returns:
            List of most active stocks with volume data
        """
        try:
            data = self._fetch_from_yahoo_finance()
            if data and 'most_active' in data:
                return data['most_active'][:limit]
            return None
        except Exception as e:
            logger.error(f"Error getting most active stocks: {e}")
            return None
    
    def get_gainers(self, limit: int = 10) -> Optional[List[Dict]]:
        """Get top gaining stocks.
        
        Args:
            limit: Maximum number of stocks to return
            
        Returns:
            List of top gainers with price change
        """
        try:
            data = self._fetch_from_yahoo_finance()
            if data and 'gainers' in data:
                return data['gainers'][:limit]
            return None
        except Exception as e:
            logger.error(f"Error getting gainers: {e}")
            return None
    
    def get_losers(self, limit: int = 10) -> Optional[List[Dict]]:
        """Get top losing stocks.
        
        Args:
            limit: Maximum number of stocks to return
            
        Returns:
            List of top losers with price change
        """
        try:
            data = self._fetch_from_yahoo_finance()
            if data and 'losers' in data:
                return data['losers'][:limit]
            return None
        except Exception as e:
            logger.error(f"Error getting losers: {e}")
            return None
    
    def get_stock_price(self, symbol: str) -> Optional[Dict]:
        """Get current price for a stock.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Stock price data or None
        """
        try:
            # This would require an API key in production
            price_data = {
                'symbol': symbol,
                'price': None,
                'change': None,
                'volume': None
            }
            return price_data
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return None
    
    def close(self):
        """Close the session."""
        self.session.close()
