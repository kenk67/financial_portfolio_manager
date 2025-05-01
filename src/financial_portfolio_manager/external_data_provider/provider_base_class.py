from abc import ABC, abstractmethod


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
