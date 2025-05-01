import requests
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import json


class DataProviderInterface(ABC):
    """Abstract base class for data providers (following Interface Segregation)."""

    @abstractmethod
    def get_current_price(self, symbol):
        """Get current price for a given symbol."""
        pass

    @abstractmethod
    def get_historical_prices(self, symbol, start_date, end_date):
        """Get historical prices for a date range."""
        pass

    @abstractmethod
    def get_company_info(self, symbol):
        """Get company information."""
        pass


class AlphaVantageProvider(DataProviderInterface):
    """Implementation using Alpha Vantage API."""

    def __init__(self, api_key):
        self._api_key = 'API KEY'
        self._base_url = "https://www.alphavantage.co/query"

    def get_current_price(self, symbol):
        """Get the current market price for a symbol."""
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self._api_key
        }

        try:
            response = requests.get(self._base_url, params=params)
            data = response.json()

            # Check for error responses
            if "Error Message" in data:
                raise ValueError(f"API Error: {data['Error Message']}")

            # Extract price from response
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                return float(data["Global Quote"]["05. price"])
            else:
                raise ValueError(f"Unexpected API response format: {data}")
        except Exception as e:
            print(f"Error fetching price for {symbol}: {str(e)}")
            # Return None or a default value in case of error
            return None

    def get_historical_prices(self, symbol, start_date, end_date):
        """Get historical daily prices for a date range."""
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "full",
            "apikey": self._api_key
        }

        try:
            response = requests.get(self._base_url, params=params)
            data = response.json()

            # Check for error responses
            if "Error Message" in data:
                raise ValueError(f"API Error: {data['Error Message']}")

            # Extract and filter historical data
            if "Time Series (Daily)" in data:
                time_series = data["Time Series (Daily)"]

                # Convert dates to strings in the format used by the API
                start_str = start_date.strftime("%Y-%m-%d")
                end_str = end_date.strftime("%Y-%m-%d")

                # Filter and convert to the desired format
                historical_prices = {}
                for date_str, values in time_series.items():
                    # Only include dates within our range
                    if start_str <= date_str <= end_str:
                        # Convert the date string to a datetime object
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        # Store the closing price
                        historical_prices[date_obj] = float(values["4. close"])

                return historical_prices
            else:
                raise ValueError(f"Unexpected API response format: {data}")
        except Exception as e:
            print(f"Error fetching historical prices for {symbol}: {str(e)}")
            # Return empty dict in case of error
            return {}

    def get_company_info(self, symbol):
        """Get company overview information."""
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self._api_key
        }

        try:
            response = requests.get(self._base_url, params=params)
            data = response.json()

            # Check for error responses
            if "Error Message" in data:
                raise ValueError(f"API Error: {data['Error Message']}")

            # Return the full company info
            return data
        except Exception as e:
            print(f"Error fetching company info for {symbol}: {str(e)}")
            # Return empty dict in case of error
            return {}


class MockDataProvider(DataProviderInterface):
    """Mock data provider for testing without API calls."""

    def __init__(self):
        # Sample data for demonstration
        self._mock_data = {
            "AAPL": {
                "name": "Apple Inc.",
                "current_price": 175.50,
                "historical": self._generate_mock_history(150.0, 180.0)
            },
            "MSFT": {
                "name": "Microsoft Corporation",
                "current_price": 305.25,
                "historical": self._generate_mock_history(280.0, 310.0)
            },
            "AMZN": {
                "name": "Amazon.com Inc.",
                "current_price": 132.80,
                "historical": self._generate_mock_history(120.0, 140.0)
            }
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
        return {date: price for date, price in historical.items()
                if start_date <= date <= end_date}

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
            "MarketCapitalization": "2000000000"
        }


# Factory pattern for creating data providers
class DataProviderFactory:
    """Factory for creating data providers."""

    @staticmethod
    def create_provider(provider_type, **kwargs):
        """Create and return a data provider of the specified type."""
        if provider_type.lower() == "alphavantage":
            if "api_key" not in kwargs:
                raise ValueError("API key required for Alpha Vantage provider")
            return AlphaVantageProvider(kwargs["api_key"])
        elif provider_type.lower() == "mock":
            return MockDataProvider()
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")