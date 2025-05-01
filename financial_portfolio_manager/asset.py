class Asset:
    """
    Base class for financial assets with encapsulation.
    """

    def __init__(self, symbol, name, asset_type):
        self._symbol = symbol  # Encapsulated attribute
        self._name = name  # Encapsulated attribute
        self._asset_type = asset_type  # Encapsulated attribute
        self._current_price = 0.0
        self._historical_prices = {}

    # Getters (property decorators for encapsulation)
    @property
    def symbol(self):
        return self._symbol

    @property
    def name(self):
        return self._name

    @property
    def asset_type(self):
        return self._asset_type

    @property
    def current_price(self):
        return self._current_price

    # Setter with validation (encapsulation)
    @current_price.setter
    def current_price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._current_price = value

    def update_price(self, price, date=None):
        """Update the current price and add to historical data."""
        self.current_price = price
        if date:
            self._historical_prices[date] = price

    def get_historical_prices(self):
        """Return a copy of historical prices (encapsulation)."""
        return self._historical_prices.copy()

    def __str__(self):
        return f"{self.name} ({self.symbol}): ${self.current_price:.2f}"


class Stock(Asset):
    """
    Stock class extending the Asset base class.
    """

    def __init__(self, symbol, name, exchange="NYSE"):
        super().__init__(symbol, name, "STOCK")
        self._exchange = exchange
        self._dividend_yield = 0.0

    @property
    def exchange(self):
        return self._exchange

    @property
    def dividend_yield(self):
        return self._dividend_yield

    @dividend_yield.setter
    def dividend_yield(self, value):
        if value < 0:
            raise ValueError("Dividend yield cannot be negative")
        self._dividend_yield = value


class Bond(Asset):
    """
    Bond class extending the Asset base class.
    """

    def __init__(self, symbol, name, face_value, coupon_rate, maturity_date):
        super().__init__(symbol, name, "BOND")
        self._face_value = face_value
        self._coupon_rate = coupon_rate
        self._maturity_date = maturity_date

    @property
    def face_value(self):
        return self._face_value

    @property
    def coupon_rate(self):
        return self._coupon_rate

    @property
    def maturity_date(self):
        return self._maturity_date

    def calculate_yield_to_maturity(self):
        """Calculate and return the yield to maturity."""
        # Simplified calculation for illustration
        # In a real application, this would be more complex
        if self.current_price > 0:
            return (self._coupon_rate * self._face_value +
                    (self._face_value - self.current_price) /
                    self._remaining_years()) / self.current_price
        return 0

    def _remaining_years(self):
        """Helper method to calculate remaining years to maturity."""
        # In a real implementation, this would calculate based on the maturity date
        # For simplicity, we'll just return a placeholder value
        return 5