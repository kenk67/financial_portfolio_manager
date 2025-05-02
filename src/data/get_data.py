from pathlib import Path

from src.financial_portfolio_manager.external_data_provider.alpha_vantage_provider import (
    AlphaVantageProvider,
)

current_dir = Path(__file__).parent

ticker_symbols = ["IBM", "AAPL", "MSFT", "GOOGL", "AMZN", "NFLX", "NVDA", "AMD", "INTC"]

provider = AlphaVantageProvider()

for symbol in ticker_symbols:
    print(f"\nProcessing data for {symbol}:")
    data = provider.get_historical_prices(symbol=symbol, datatype="csv")

    try:
        file_path = current_dir / f"{symbol}.csv"
        file_path.write_text(data.text)
        print(f"Data successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing CSV for {symbol}: {e}")
