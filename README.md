# StockTwits Most Active Equities Analyzer

An automated Python pipeline that fetches the most active stocks from StockTwits, performs technical analysis via screenshots, and generates AI-powered insights using multiple LLM providers (Perplexity, Claude, Google AI).

## 🎯 Workflow Overview

**Step 1: Fetch Market Data** → **Step 2: Export & Trigger Automation** → **DesktopAuto.exe** (Screenshot + LLM Analysis)

1. Fetch top 10 most active equities with real-time prices & volumes
2. Save symbols to file  
3. Launch DesktopAuto.exe with proper working directory configuration
4. DesktopAuto captures 4 technical analysis views per symbol (TradingView)
5. Captures Symbolik.com sentiment data
6. Runs LLM analysis on screenshots (Perplexity, Claude, Google AI)
7. Generates AI insights and sends email alerts

## 📊 Key Features

- **Real-time Market Data**: Fetches most active stocks with live prices and volumes
- **Automated Chart Capture**: Screenshots 4 different technical analysis views per symbol
- **Multi-LLM Analysis**: Leverages Perplexity, Claude, and Google AI for chart interpretation
- **Email Alerts**: Sends analysis alerts when thresholds are met
- **One-Command Execution**: Single python src/main.py runs entire pipeline

## 🚀 Quick Start

`ash
git clone https://github.com/mskpairprogrammer/stocktwits_most_active.git
cd stocktwits_most_active
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/main.py
`

## 📁 Project Structure

`
src/
├── main.py              # Orchestrator (Step 1 & 2)
├── market_data.py       # Fetch active stocks
├── export_stocks.py     # Export & trigger automation
├── market_movers.py     # Display market data
├── analyzer.py          # Legacy: Symbol analysis
└── scraper.py           # Legacy: API scraping
`

## 🔧 How It Works

### Step 1: `market_data.py` - MarketDataFetcher
- Fetches top 10 most active equities
- Returns: symbol, name, price, change %, volume

### Step 2: `export_stocks.py` - extract_and_save_stocks()
1. Extract top 10 symbols from market data
2. Save to: stock_symbols.txt (one symbol per line)
3. **Launch DesktopAuto.exe with proper config:**
   `python
   subprocess.Popen(
       [desktop_auto_path],
       cwd=desktop_auto_dir,                    # Working directory
       creationflags=subprocess.CREATE_NEW_CONSOLE  # Console environment
   )
   `

**Critical:** Working directory allows DesktopAuto.exe to find .env file with API keys

### DesktopAuto.exe Integration

1. **TradingView Charts (4 tabs):**
   - Trend Analysis (Luxo Algo)
   - Smoothed Heiken Ashi Candles
   - Volume Layout
   - Volume Profile (RVOL)

2. **Symbolik.com Analysis:**
   - Additional sentiment/technical data

3. **LLM Analysis on Screenshots:**
   - Perplexity (sonar-pro)
   - Claude (claude-sonnet-4-5-20250929)
   - Google AI (gemini-3-pro-preview)

4. **Output:**
   - Screenshots per symbol
   - AI analysis results
   - Email alerts

## 🛠️ The Fix: Why LLM API Calls Weren't Triggering

**Problem:** DesktopAuto.exe ran but skipped LLM analysis

**Root Cause:** No working directory set → .env file not found → API keys not loaded

**Solution:** Set working directory in subprocess call:
`python
subprocess.Popen(
    [desktop_auto_path],
    cwd=desktop_auto_dir,
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
`

This allows DesktopAuto.exe to:
- Find .env file in correct location
- Load API credentials (Perplexity, Claude, Google)
- Execute LLM analysis pipeline

## 📊 Sample Output

`
StockTwits Most Active Equities Analyzer

[Step 1] Fetching Most Active Equities...
✓ Found 10 most active equities
✓ Top Gainer: SMX (+231.11%)
✓ Top Loser: NVDA (-2.01%)

[Most Active Equities - Top 10]
Rank   Symbol   Company          Price      % Change   Volume
────────────────────────────────────────────────────────────
1      SPY      SPDR S&P 500    .58     +0.57%     49.21M
2      DJT      Trump Media     .66      +5.29%     4.44M
3      NVDA     NVIDIA Corp     .64     -2.01%     121.33M
4      QQQ      Invesco QQQ     .11     +0.79%     23.03M
5      SMX      SMX Security    .02      +231.11%   22.54M
6      TSLA     Tesla Inc       .25     +0.86%     36.25M
7      INTC     Intel Corp      .78      +10.73%    95.8M
8      IBRX     ImmunelyBio     .40       +12.49%    21.34M
9      MSTR     Strategy        .40     +1.57%     15.11M
10     ALT      Altimmune       .22       +1.03%     2.12M

[Step 2] Export Symbols & Trigger Automation...
✓ Active stocks extracted and saved
✓ Total records: 10 most active + 5 gainers + 4 losers
✓ DesktopAuto.exe triggered
`

## 🔑 Dependencies

- requests
- beautifulsoup4
- pandas
- python-dotenv

## 📚 Legacy Modules (Not in Active Workflow)

- **analyzer.py** - Community post symbol extraction
- **scraper.py** - StockTwits API scraping
- **market_movers.py** - Display function

## 📞 Support

For issues, create a GitHub issue.

## 📄 License

MIT

---

**Last Updated:** November 29, 2025
