"""Analyzer for identifying frequently mentioned stock symbols."""

import re
from collections import Counter
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class SymbolAnalyzer:
    """Analyzes text to identify and count stock symbol mentions."""
    
    # Pattern to match stock symbols (1-4 uppercase letters)
    SYMBOL_PATTERN = re.compile(r'\b[A-Z]{1,4}\b')
    
    # Common non-stock words to filter out
    COMMON_WORDS = {
        'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'CAN', 'ALL', 'WILL',
        'YOUR', 'ONE', 'OUT', 'HAD', 'HAS', 'WAS', 'WERE', 'BEEN', 'HAVE', 'MAY',
        'SAID', 'USE', 'GET', 'MAKE', 'GO', 'KNOW', 'TAKE', 'SEE', 'COME', 'THINK',
        'BECAUSE', 'JUST', 'ALSO', 'OVER', 'SUCH', 'BACK', 'EVEN', 'ONLY', 'YEAR',
        'THAN', 'WHEN', 'THEN', 'WHO', 'WHAT', 'WHICH', 'WHY', 'HOW', 'IF', 'AS',
        'TO', 'FROM', 'BY', 'WITH', 'IN', 'ON', 'AT', 'OF', 'UP', 'OR', 'SO', 'DO',
        'NO', 'DOWN', 'SOME', 'ANY', 'EACH', 'BOTH', 'VERY', 'MORE', 'MOST', 'MUCH',
        'TOO', 'JUST', 'NOW', 'ABOUT', 'AFTER', 'BEFORE', 'BETWEEN', 'DURING',
        # Single letters (not valid stock symbols)
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    }
    
    def __init__(self, min_length: int = 1, max_length: int = 4):
        """Initialize the analyzer.
        
        Args:
            min_length: Minimum symbol length
            max_length: Maximum symbol length
        """
        self.min_length = min_length
        self.max_length = max_length
    
    def extract_symbols(self, text: str) -> List[str]:
        """Extract potential stock symbols from text.
        
        Args:
            text: Input text to search
            
        Returns:
            List of extracted symbols
        """
        if not text:
            return []
        
        matches = self.SYMBOL_PATTERN.findall(text)
        # Filter out common words and respect length constraints
        symbols = [
            s for s in matches
            if self.min_length <= len(s) <= self.max_length
            and s not in self.COMMON_WORDS
        ]
        return symbols
    
    def analyze_mentions(self, texts: List[str], top_n: int = 10) -> List[Tuple[str, int]]:
        """Analyze symbol mentions across multiple texts.
        
        Args:
            texts: List of texts to analyze
            top_n: Number of top symbols to return
            
        Returns:
            List of (symbol, count) tuples sorted by frequency
        """
        all_symbols = []
        
        for text in texts:
            symbols = self.extract_symbols(text)
            all_symbols.extend(symbols)
        
        if not all_symbols:
            return []
        
        counter = Counter(all_symbols)
        return counter.most_common(top_n)
    
    def get_statistics(self, texts: List[str]) -> Dict:
        """Get statistics about symbol mentions.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            Dictionary with analysis statistics
        """
        all_symbols = []
        for text in texts:
            symbols = self.extract_symbols(text)
            all_symbols.extend(symbols)
        
        unique_symbols = set(all_symbols)
        
        return {
            'total_mentions': len(all_symbols),
            'unique_symbols': len(unique_symbols),
            'average_mentions_per_text': len(all_symbols) / len(texts) if texts else 0,
            'most_common': Counter(all_symbols).most_common(5) if all_symbols else []
        }
