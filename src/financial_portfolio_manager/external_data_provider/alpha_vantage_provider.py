from datetime import datetime

import httpx

from src.financial_portfolio_manager.external_data_provider.provider_base_class import (
    DataProviderInterface,
)
from src.financial_portfolio_manager.settings import get_settings

settings = get_settings()


class AlphaVantageProvider(DataProviderInterface):
    """Implementation using Alpha Vantage API."""

    def __init__(self):
        self._base_urls = settings.DATA_PROVIDER_URL.get("ALPHA_VANTAGE")

    def get_current_price(self, symbol):
        """Get the current market price for a symbol."""
        params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": self._api_key}

        try:
            response = httpx.get(self._base_url, params=params)
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
            "apikey": self._api_key,
        }

        try:
            response = httpx.get(self._base_url, params=params)
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
        params = {"function": "OVERVIEW", "symbol": symbol, "apikey": self._api_key}

        try:
            response = httpx.get(self._base_url, params=params)
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
