from datetime import date

import httpx

from src.financial_portfolio_manager.external_data_provider.provider_base_class import (
    DataProviderInterface,
)
from src.financial_portfolio_manager.models.alpha_vantage import (
    GlobalQuote,
    CompanyOverview,
    AlphaVantageTimeSeriesDaily,
)
from src.financial_portfolio_manager.settings import get_settings, get_auth_settings

settings = get_settings()
auth_settings = get_auth_settings()


class AlphaVantageProvider(DataProviderInterface):
    """Implementation using Alpha Vantage API."""

    def __init__(self):
        self._base_url = settings.DATA_PROVIDER_URL.get("ALPHA_VANTAGE")

    def get_api_data(self, function: str, symbol: str, **kwargs) -> dict:
        """Get API data."""
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": auth_settings.ALPHA_VANTAGE_API_KEY,
        }

        if "outputsize" in kwargs:
            params["outputsize"] = kwargs["outputsize"]

        try:
            response = httpx.get(self._base_url, params=params)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise e

    def get_current_price(self, symbol: str) -> float:
        """Get the current market price for a symbol."""

        response_data = self.get_api_data(function="GLOBAL_QUOTE", symbol=symbol)
        data = GlobalQuote(**response_data)
        return data.price

    def get_historical_prices(self, symbol, start_date: date, end_date: date) -> dict:
        """Get historical daily close prices for a date range."""

        response_data = self.get_api_data(
            function="TIME_SERIES_DAILY", symbol=symbol, outputsize="compact"
        )

        data = AlphaVantageTimeSeriesDaily(**response_data)
        historical_prices = {
            daily_date: data.close
            for daily_date, data in data.time_series.items()
            if start_date <= daily_date <= end_date
        }

        return historical_prices

    def get_company_info(self, symbol: str) -> CompanyOverview:
        """Get company overview information."""

        response_data = self.get_api_data(function="OVERVIEW", symbol=symbol)
        data = CompanyOverview(**response_data)
        return data
