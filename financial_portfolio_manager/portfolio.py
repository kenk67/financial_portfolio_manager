from collections import defaultdict


class Portfolio:
    """
    Portfolio class that aggregates assets and tracks transactions.
    Demonstrates aggregation principle.
    """

    def __init__(self, name, owner):
        self._name = name
        self._owner = owner
        self._holdings = {}  # Maps asset symbol to (asset object, quantity)
        self._transactions = []
        self._cash_balance = 0.0

    @property
    def name(self):
        return self._name

    @property
    def owner(self):
        return self._owner

    @property
    def cash_balance(self):
        return self._cash_balance

    @cash_balance.setter
    def cash_balance(self, value):
        self._cash_balance = value

    def add_cash(self, amount):
        """Add cash to the portfolio."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._cash_balance += amount

    def withdraw_cash(self, amount):
        """Withdraw cash from the portfolio."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self._cash_balance:
            raise ValueError("Insufficient funds")
        self._cash_balance -= amount

    def add_asset(self, asset, quantity, price=None):
        """Add an asset to the portfolio."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        # If we already have this asset, update quantity
        if asset.symbol in self._holdings:
            current_asset, current_quantity = self._holdings[asset.symbol]
            self._holdings[asset.symbol] = (current_asset, current_quantity + quantity)
        else:
            self._holdings[asset.symbol] = (asset, quantity)

        # If price is provided, update asset price
        if price is not None:
            asset.current_price = price

    def remove_asset(self, symbol, quantity):
        """Remove an asset from the portfolio."""
        if symbol not in self._holdings:
            raise ValueError(f"Asset {symbol} not in portfolio")

        current_asset, current_quantity = self._holdings[symbol]
        if quantity > current_quantity:
            raise ValueError(f"Cannot remove {quantity} of {symbol}, only have {current_quantity}")

        # Update holdings
        if quantity == current_quantity:
            del self._holdings[symbol]
        else:
            self._holdings[symbol] = (current_asset, current_quantity - quantity)

    def add_transaction(self, transaction):
        """Record a transaction in the portfolio."""
        self._transactions.append(transaction)

    def get_holdings(self):
        """Get a copy of all holdings."""
        return {symbol: (asset, quantity) for symbol, (asset, quantity) in self._holdings.items()}

    def get_transactions(self, from_date=None, to_date=None, asset_symbol=None):
        """Get filtered transactions."""
        filtered = self._transactions

        if from_date:
            filtered = [t for t in filtered if t.date >= from_date]
        if to_date:
            filtered = [t for t in filtered if t.date <= to_date]
        if asset_symbol:
            filtered = [t for t in filtered if t.asset_symbol == asset_symbol]

        return filtered

    def total_value(self):
        """Calculate the total portfolio value including cash."""
        asset_value = sum(asset.current_price * quantity
                          for symbol, (asset, quantity) in self._holdings.items())
        return asset_value + self._cash_balance

    def asset_allocation(self):
        """Calculate asset allocation as percentages."""
        total = self.total_value()
        if total == 0:
            return {"cash": 100.0}

        allocation = {"cash": (self._cash_balance / total) * 100}

        # Group by asset type
        by_type = defaultdict(float)
        for symbol, (asset, quantity) in self._holdings.items():
            value = asset.current_price * quantity
            by_type[asset.asset_type] += value

        # Calculate percentages
        for asset_type, value in by_type.items():
            allocation[asset_type.lower()] = (value / total) * 100

        return allocation

    def performance(self, start_date, end_date):
        """Calculate portfolio performance between dates."""
        # This would use historical data to calculate returns
        # In a real application, this would be more complex
        return 0.0  # Placeholder

    def __str__(self):
        return (f"Portfolio: {self._name}\nOwner: {self._owner}\n"
                f"Total Value: ${self.total_value():.2f}\n"
                f"Cash Balance: ${self._cash_balance:.2f}\n"
                f"Number of Assets: {len(self._holdings)}")