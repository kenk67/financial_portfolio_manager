from datetime import datetime, timedelta

from src.financial_portfolio_manager.external_data_provider.provider_base_class import (
    DataProviderInterface,
)


class MockDataProvider(DataProviderInterface):
    """Mock data provider for testing without API calls."""

    def __init__(self):
        # Sample data for demonstration
        self._mock_data = {
            "AAPL": {
                "name": "Apple Inc.",
                "current_price": 175.50,
                "historical": self._generate_mock_history(150.0, 180.0),
            },
            "MSFT": {
                "name": "Microsoft Corporation",
                "current_price": 305.25,
                "historical": self._generate_mock_history(280.0, 310.0),
            },
            "AMZN": {
                "name": "Amazon.com Inc.",
                "current_price": 132.80,
                "historical": self._generate_mock_history(120.0, 140.0),
            },
        }

    def _generate_mock_history(self, min_price, max_price):
        """Generate mock historical data for the past 30 days."""
        import random

        today = datetime.now()
        history = {}

        for i in range(30):
            date = today - timedelta(days=i)
            # Generate a random price within the given range
            price = round(random.uniform(min_price, max_price), 2)
            history[date] = price

        return history

    def get_current_price(self, symbol):
        """Get current mock price for a symbol."""
        symbol = symbol.upper()
        if symbol in self._mock_data:
            return self._mock_data[symbol]["current_price"]
        return None

    def get_historical_prices(self, symbol, start_date, end_date):
        """Get mock historical prices for a date range."""
        symbol = symbol.upper()
        if symbol not in self._mock_data:
            return {}

        # Filter historical data for the date range
        historical = self._mock_data[symbol]["historical"]
        return {
            date: price
            for date, price in historical.items()
            if start_date <= date <= end_date
        }

    def get_company_info(self, symbol):
        """Get mock company information."""
        symbol = symbol.upper()
        if symbol not in self._mock_data:
            return {}

        return {
            "Symbol": symbol,
            "Name": self._mock_data[symbol]["name"],
            "Description": f"Mock description for {self._mock_data[symbol]['name']}",
            "Sector": "Technology",
            "Industry": "Consumer Electronics",
            "MarketCapitalization": "2000000000",
        }
