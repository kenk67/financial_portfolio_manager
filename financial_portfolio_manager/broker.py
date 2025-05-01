from abc import ABC, abstractmethod
from .transaction import Transaction, TransactionType


class BrokerInterface(ABC):
    """
    Abstract broker interface following the Interface Segregation Principle (SOLID).
    """

    @abstractmethod
    def execute_buy(self, portfolio, asset_symbol, quantity, price):
        """Execute a buy transaction."""
        pass

    @abstractmethod
    def execute_sell(self, portfolio, asset_symbol, quantity, price):
        """Execute a sell transaction."""
        pass

    @abstractmethod
    def get_current_price(self, asset_symbol):
        """Get the current market price for an asset."""
        pass

    @abstractmethod
    def get_historical_prices(self, asset_symbol, start_date, end_date):
        """Get historical prices for an asset."""
        pass


class SimpleBroker(BrokerInterface):
    """
    A simple broker implementation with a fixed fee structure.
    """

    def __init__(self, name, fee_per_trade=9.99):
        self._name = name
        self._fee_per_trade = fee_per_trade

    @property
    def name(self):
        return self._name

    @property
    def fee_per_trade(self):
        return self._fee_per_trade

    def execute_buy(self, portfolio, asset_symbol, quantity, price):
        """Execute a buy transaction."""
        # Calculate total cost
        total_cost = quantity * price + self._fee_per_trade

        # Check if portfolio has enough cash
        if portfolio.cash_balance < total_cost:
            raise ValueError(f"Insufficient funds. Need ${total_cost:.2f}, have ${portfolio.cash_balance:.2f}")

        # Create transaction
        transaction = Transaction(
            asset_symbol=asset_symbol,
            transaction_type=TransactionType.BUY,
            quantity=quantity,
            price=price
        )
        transaction.fees = self._fee_per_trade

        # Add transaction to portfolio
        portfolio.add_transaction(transaction)

        # Try to find the asset in the portfolio's holdings
        holdings = portfolio.get_holdings()
        if asset_symbol in holdings:
            asset = holdings[asset_symbol][0]
            # Update asset with new quantity
            portfolio.add_asset(asset, quantity, price)
        else:
            # For simplicity, we'll assume the asset should already exist in portfolio
            # In a real implementation, we would either create it or fetch it from a repository
            raise ValueError(f"Asset {asset_symbol} not found in portfolio")

        # Deduct cost from portfolio
        portfolio.withdraw_cash(total_cost)

        return transaction

    def execute_sell(self, portfolio, asset_symbol, quantity, price):
        """Execute a sell transaction."""
        # Check if portfolio has the asset in sufficient quantity
        holdings = portfolio.get_holdings()
        if asset_symbol not in holdings:
            raise ValueError(f"Asset {asset_symbol} not found in portfolio")

        asset, owned_quantity = holdings[asset_symbol]
        if quantity > owned_quantity:
            raise ValueError(f"Insufficient quantity. Have {owned_quantity}, trying to sell {quantity}")

        # Calculate proceeds
        proceeds = quantity * price - self._fee_per_trade

        # Create transaction
        transaction = Transaction(
            asset_symbol=asset_symbol,
            transaction_type=TransactionType.SELL,
            quantity=quantity,
            price=price
        )
        transaction.fees = self._fee_per_trade

        # Add transaction to portfolio
        portfolio.add_transaction(transaction)

        # Remove assets from portfolio
        portfolio.remove_asset(asset_symbol, quantity)

        # Add proceeds to portfolio cash
        portfolio.add_cash(proceeds)

        return transaction

    def get_current_price(self, asset_symbol):
        """
        Get the current market price for an asset.
        In a real implementation, this would call a financial data API.
        """
        # Placeholder implementation
        # In a real application, this would fetch data from an API
        return 100.0  # Dummy price

    def get_historical_prices(self, asset_symbol, start_date, end_date):
        """
        Get historical prices for an asset.
        In a real implementation, this would call a financial data API.
        """
        # Placeholder implementation
        # In a real application, this would fetch data from an API
        return {start_date: 95.0, end_date: 105.0}  # Dummy data