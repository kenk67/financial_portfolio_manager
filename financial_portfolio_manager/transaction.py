from datetime import datetime
from enum import Enum, auto


class TransactionType(Enum):
    """Enum for transaction types."""
    BUY = auto()
    SELL = auto()
    DIVIDEND = auto()
    INTEREST = auto()
    DEPOSIT = auto()
    WITHDRAWAL = auto()


class Transaction:
    """
    Transaction class to record financial activities.
    """

    def __init__(self, asset_symbol, transaction_type, quantity, price, date=None):
        self._id = self._generate_id()
        self._asset_symbol = asset_symbol
        self._transaction_type = transaction_type
        self._quantity = quantity
        self._price = price
        self._date = date if date else datetime.now()
        self._fees = 0.0

    def _generate_id(self):
        """Generate a unique transaction ID."""
        # In a real application, this would generate a truly unique ID
        return f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    @property
    def id(self):
        return self._id

    @property
    def asset_symbol(self):
        return self._asset_symbol

    @property
    def transaction_type(self):
        return self._transaction_type

    @property
    def quantity(self):
        return self._quantity

    @property
    def price(self):
        return self._price

    @property
    def date(self):
        return self._date

    @property
    def fees(self):
        return self._fees

    @fees.setter
    def fees(self, value):
        if value < 0:
            raise ValueError("Fees cannot be negative")
        self._fees = value

    @property
    def total_value(self):
        """Calculate the total transaction value including fees."""
        return self._quantity * self._price + self._fees

    def __str__(self):
        action = "Bought" if self._transaction_type == TransactionType.BUY else "Sold"
        return (f"{action} {self._quantity} of {self._asset_symbol} @ ${self._price:.2f} "
                f"on {self._date.strftime('%Y-%m-%d')} (Total: ${self.total_value:.2f})")