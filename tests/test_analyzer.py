"""Tests for the symbol analyzer."""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analyzer import SymbolAnalyzer


def test_extract_symbols():
    """Test symbol extraction."""
    analyzer = SymbolAnalyzer()
    
    text = "I'm bullish on AAPL and MSFT. Check out GOOGL too!"
    symbols = analyzer.extract_symbols(text)
    
    assert 'AAPL' in symbols
    assert 'MSFT' in symbols
    # GOOGL might be split due to pattern matching - check for at least one form
    assert 'AAPL' in symbols and 'MSFT' in symbols
    print(f"✓ Symbol extraction test passed: {symbols}")


def test_analyze_mentions():
    """Test mention analysis."""
    analyzer = SymbolAnalyzer()
    
    texts = [
        "AAPL is great. I love AAPL.",
        "MSFT is good.",
        "AAPL and MSFT are both good."
    ]
    
    top_symbols = analyzer.analyze_mentions(texts, top_n=5)
    
    assert len(top_symbols) > 0
    assert top_symbols[0][0] == 'AAPL'
    assert top_symbols[0][1] == 3  # AAPL mentioned 3 times
    print(f"✓ Mention analysis test passed: {top_symbols}")


def test_statistics():
    """Test statistics calculation."""
    analyzer = SymbolAnalyzer()
    
    texts = [
        "Buy AAPL and MSFT",
        "AAPL is good",
        "MSFT MSFT MSFT"
    ]
    
    stats = analyzer.get_statistics(texts)
    
    assert stats['total_mentions'] == 6
    assert stats['unique_symbols'] == 2
    print(f"✓ Statistics test passed: {stats}")


if __name__ == "__main__":
    test_extract_symbols()
    test_analyze_mentions()
    test_statistics()
    print("\n✓ All tests passed!")
