from abc import ABC, abstractmethod

from residue_files.methods import MockDataProvider
from src.financial_portfolio_manager.external_data_provider.alpha_vantage_provider import (
    AlphaVantageProvider,
)


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
