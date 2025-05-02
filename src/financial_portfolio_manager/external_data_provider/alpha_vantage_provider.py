from typing import Union

import httpx
from httpx import Response

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

    def get_api_data(
        self, function: str, symbol: str, return_raw: bool = False, **kwargs
    ) -> Union[dict, Response]:
        """
        Get API data.

        Args:
            function: Alpha Vantage function to call
            symbol: Stock symbol
            return_raw: If True, returns the raw Response object, otherwise returns parsed JSON
            **kwargs: Additional parameters to pass to the API
        """
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": auth_settings.ALPHA_VANTAGE_API_KEY,
        }

        for param in ["outputsize", "datatype"]:
            if param in kwargs:
                params[param] = kwargs[param]

        try:
            response = httpx.get(self._base_url, params=params)
            response.raise_for_status()
            return response if return_raw else response.json()

        except Exception as e:
            raise e

    def get_current_price(self, symbol: str) -> float:
        """Get the current market price for a symbol."""

        response_data = self.get_api_data(function="GLOBAL_QUOTE", symbol=symbol)
        data = GlobalQuote(**response_data)
        return data.price

    def get_historical_prices(self, symbol, **kwargs):
        """Get historical daily close prices for a date range."""

        if "datatype" in kwargs:
            return self.get_api_data(
                function="TIME_SERIES_DAILY",
                symbol=symbol,
                outputsize="full",
                return_raw=True,
                **kwargs
            )

        response_data = self.get_api_data(
            function="TIME_SERIES_DAILY", symbol=symbol, outputsize="compact"
        )

        data = AlphaVantageTimeSeriesDaily(**response_data)
        historical_prices = {
            daily_date: data.close for daily_date, data in data.time_series.items()
        }

        return historical_prices

    def get_company_info(self, symbol: str) -> CompanyOverview:
        """Get company overview information."""

        response_data = self.get_api_data(function="OVERVIEW", symbol=symbol)
        data = CompanyOverview(**response_data)
        return data
