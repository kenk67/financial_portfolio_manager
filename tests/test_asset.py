import unittest
from datetime import datetime

from financial_portfolio_manager.asset import Asset, Stock, Bond


class TestAsset(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.asset = Asset("TEST", "Test Asset", "GENERIC")

    def test_initialization(self):
        """Test asset initialization."""
        self.assertEqual(self.asset.symbol, "TEST")
        self.assertEqual(self.asset.name, "Test Asset")
        self.assertEqual(self.asset.asset_type, "GENERIC")
        self.assertEqual(self.asset.current_price, 0.0)

    def test_update_price(self):
        """Test updating asset price."""
        self.asset.update_price(100.0)
        self.assertEqual(self.asset.current_price, 100.0)

        # Test with date
        self.asset.update_price(110.0, datetime(2025, 1, 1))
        self.assertEqual(self.asset.current_price, 110.0)

        historical_prices = self.asset.get_historical_prices()
        self.assertEqual(historical_prices[datetime(2025, 1, 1)], 110.0)

    def test_negative_price_validation(self):
        """Test validation prevents negative prices."""
        with self.assertRaises(ValueError):
            self.asset.current_price = -10.0

    def test_string_representation(self):
        """Test string representation."""
        self.asset.current_price = 42.50
        self.assertEqual(str(self.asset), "Test Asset (TEST): $42.50")


class TestStock(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.stock = Stock("AAPL", "Apple Inc.", "NASDAQ")

    def test_initialization(self):
        """Test stock initialization."""
        self.assertEqual(self.stock.symbol, "AAPL")
        self.assertEqual(self.stock.name, "Apple Inc.")
        self.assertEqual(self.stock.asset_type, "STOCK")
        self.assertEqual(self.stock.exchange, "NASDAQ")
        self.assertEqual(self.stock.dividend_yield, 0.0)

    def test_dividend_yield(self):
        """Test setting dividend yield."""
        self.stock.dividend_yield = 0.025  # 2.5%
        self.assertEqual(self.stock.dividend_yield, 0.025)

        # Test validation
        with self.assertRaises(ValueError):
            self.stock.dividend_yield = -0.01


class TestBond(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.maturity_date = datetime(2030, 1, 1)
        self.bond = Bond("T10Y", "10-Year Treasury", 1000.0, 0.03, self.maturity_date)

    def test_initialization(self):
        """Test bond initialization."""
        self.assertEqual(self.bond.symbol, "T10Y")
        self.assertEqual(self.bond.name, "10-Year Treasury")
        self.assertEqual(self.bond.asset_type, "BOND")
        self.assertEqual(self.bond.face_value, 1000.0)
        self.assertEqual(self.bond.coupon_rate, 0.03)
        self.assertEqual(self.bond.maturity_date, self.maturity_date)

    def test_yield_to_maturity(self):
        """Test yield to maturity calculation."""
        # Set current price for YTM calculation
        self.bond.current_price = 950.0
        ytm = self.bond.calculate_yield_to_maturity()
        self.assertGreater(ytm, 0)


if __name__ == "__main__":
    unittest.main()
