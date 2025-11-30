"""Scraper for fetching StockTwits community posts."""

import requests
from typing import List, Dict, Optional
import logging
import time

logger = logging.getLogger(__name__)


class StockTwitsScraper:
    """Scrapes posts from StockTwits community."""
    
    BASE_URL = "https://api.stocktwits.com/api/v3"
    WEB_URL = "https://stocktwits.com"
    
    def __init__(self, timeout: int = 10):
        """Initialize the scraper.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_trending_symbols(self) -> Optional[List[Dict]]:
        """Fetch trending symbols from StockTwits.
        
        Returns:
            List of trending symbols or None if request fails
        """
        try:
            url = f"{self.BASE_URL}/trending/symbols"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("symbols", [])
        except requests.RequestException as e:
            logger.error(f"Error fetching trending symbols: {e}")
            return None
    
    def get_symbol_sentiment(self, symbol: str) -> Optional[Dict]:
        """Fetch sentiment data for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Sentiment data or None if request fails
        """
        try:
            url = f"{self.BASE_URL}/symbols/{symbol}/sentiment"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching sentiment for {symbol}: {e}")
            return None
    
    def get_most_mentioned_symbols(self, limit: int = 30) -> Optional[List[Dict]]:
        """Fetch most mentioned symbols from the community.
        
        Args:
            limit: Maximum number of symbols to return
            
        Returns:
            List of most mentioned symbols or None if request fails
        """
        try:
            url = f"{self.BASE_URL}/symbols/trending"
            params = {'limit': limit}
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("symbols", [])
        except requests.RequestException as e:
            logger.error(f"Error fetching most mentioned symbols: {e}")
            return None
    
    def get_recent_posts(self, symbol: str, limit: int = 30) -> Optional[List[Dict]]:
        """Fetch recent posts for a specific symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            limit: Maximum number of posts to return
            
        Returns:
            List of recent posts or None if request fails
        """
        try:
            url = f"{self.BASE_URL}/symbols/{symbol}/messages"
            params = {'limit': limit}
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("messages", [])
        except requests.RequestException as e:
            logger.error(f"Error fetching posts for {symbol}: {e}")
            return None
    
    def collect_community_data(self, num_symbols: int = 20) -> Dict[str, List]:
        """Collect data from top trending symbols and their recent posts.
        
        Args:
            num_symbols: Number of trending symbols to analyze
            
        Returns:
            Dictionary with symbols and their post messages
        """
        result = {'symbols': [], 'messages': []}
        
        try:
            # Get trending symbols
            trending = self.get_most_mentioned_symbols(limit=num_symbols)
            if not trending:
                logger.warning("No trending symbols found")
                return result
            
            logger.info(f"Found {len(trending)} trending symbols")
            result['symbols'] = trending
            
            # Collect recent posts from each symbol
            for symbol_data in trending:
                symbol = symbol_data.get('symbol', '')
                if not symbol:
                    continue
                
                logger.info(f"Fetching posts for {symbol}...")
                posts = self.get_recent_posts(symbol, limit=10)
                
                if posts:
                    for post in posts:
                        message = post.get('body', '')
                        if message:
                            result['messages'].append({
                                'symbol': symbol,
                                'message': message,
                                'timestamp': post.get('created_at', '')
                            })
                
                # Rate limiting
                time.sleep(0.5)
            
            logger.info(f"Collected {len(result['messages'])} messages")
            return result
            
        except Exception as e:
            logger.error(f"Error collecting community data: {e}")
            return result
    
    def close(self):
        """Close the session."""
        self.session.close()
