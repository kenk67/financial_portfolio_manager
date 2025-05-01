from src.financial_portfolio_manager.asset import Stock, Bond
from src.financial_portfolio_manager.broker import SimpleBroker
from src.financial_portfolio_manager.external_data_provider.provider_base_class import (
    DataProviderFactory,
)
from src.financial_portfolio_manager.portfolio import Portfolio
from src.financial_portfolio_manager.transaction import Transaction, TransactionType
from src.financial_portfolio_manager.visualization import PortfolioVisualizer

# # Add the project directory to Python path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FinancialPortfolioManager:
    """
    Main application class that orchestrates the financial portfolio management.
    This is the highest level of abstraction (Dependency Inversion Principle).
    """

    def __init__(self, data_provider_type="mock", api_key=None):
        """Initialize the application."""
        # Create dependencies
        self._data_provider = DataProviderFactory.create_provider(
            data_provider_type, api_key=api_key
        )
        self._broker = SimpleBroker("Sample Broker", fee_per_trade=9.99)
        self._portfolios = {}  # Dictionary to store multiple portfolios

    def create_portfolio(self, name, owner):
        """Create a new portfolio."""
        if name in self._portfolios:
            raise ValueError(f"Portfolio with name '{name}' already exists")

        portfolio = Portfolio(name, owner)
        self._portfolios[name] = portfolio
        return portfolio

    def create_stock(self, symbol, name=None, exchange="NYSE"):
        """Create a stock asset with data from the provider."""
        if name is None:
            # Try to get the name from company info
            company_info = self._data_provider.get_company_info(symbol)
            name = company_info.get("Name", symbol)

        # Create the stock
        stock = Stock(symbol, name, exchange)

        # Update with current price
        current_price = self._data_provider.get_current_price(symbol)
        if current_price:
            stock.current_price = current_price

        return stock

    def create_bond(self, symbol, name, face_value, coupon_rate, maturity_date):
        """Create a bond asset."""
        bond = Bond(symbol, name, face_value, coupon_rate, maturity_date)

        # Update with current price if available
        current_price = self._data_provider.get_current_price(symbol)
        if current_price:
            bond.current_price = current_price

        return bond

    def buy_asset(self, portfolio_name, asset, quantity):
        """Buy an asset for a portfolio."""
        if portfolio_name not in self._portfolios:
            raise ValueError(f"Portfolio '{portfolio_name}' not found")

        portfolio = self._portfolios[portfolio_name]

        # Get current price
        current_price = self._data_provider.get_current_price(asset.symbol)
        if not current_price:
            raise ValueError(f"Could not get current price for {asset.symbol}")

        # Add asset to portfolio first, then execute transaction
        portfolio.add_asset(asset, 0)  # Add with 0 quantity initially

        # Execute the buy transaction using the broker
        transaction = self._broker.execute_buy(
            portfolio, asset.symbol, quantity, current_price
        )

        return transaction

    def sell_asset(self, portfolio_name, asset_symbol, quantity):
        """Sell an asset from a portfolio."""
        if portfolio_name not in self._portfolios:
            raise ValueError(f"Portfolio '{portfolio_name}' not found")

        portfolio = self._portfolios[portfolio_name]

        # Check if portfolio has the asset
        holdings = portfolio.get_holdings()
        if asset_symbol not in holdings:
            raise ValueError(f"Asset '{asset_symbol}' not found in portfolio")

        # Get current price
        current_price = self._data_provider.get_current_price(asset_symbol)
        if not current_price:
            raise ValueError(f"Could not get current price for {asset_symbol}")

        # Execute the sell transaction using the broker
        transaction = self._broker.execute_sell(
            portfolio, asset_symbol, quantity, current_price
        )

        return transaction

    def deposit_cash(self, portfolio_name, amount):
        """Deposit cash into a portfolio."""
        if portfolio_name not in self._portfolios:
            raise ValueError(f"Portfolio '{portfolio_name}' not found")

        portfolio = self._portfolios[portfolio_name]
        portfolio.add_cash(amount)

        # Record as a transaction
        transaction = Transaction(
            asset_symbol="CASH",
            transaction_type=TransactionType.DEPOSIT,
            quantity=1,
            price=amount,
        )
        portfolio.add_transaction(transaction)

        return transaction

    def withdraw_cash(self, portfolio_name, amount):
        """Withdraw cash from a portfolio."""
        if portfolio_name not in self._portfolios:
            raise ValueError(f"Portfolio '{portfolio_name}' not found")

        portfolio = self._portfolios[portfolio_name]

        # Try to withdraw
        portfolio.withdraw_cash(amount)

        # Record as a transaction
        transaction = Transaction(
            asset_symbol="CASH",
            transaction_type=TransactionType.WITHDRAWAL,
            quantity=1,
            price=amount,
        )
        portfolio.add_transaction(transaction)

        return transaction

    def update_prices(self, portfolio_name):
        """Update all asset prices in a portfolio."""
        if portfolio_name not in self._portfolios:
            raise ValueError(f"Portfolio '{portfolio_name}' not found")

        portfolio = self._portfolios[portfolio_name]
        holdings = portfolio.get_holdings()

        updated_count = 0
        for symbol, (asset, _) in holdings.items():
            current_price = self._data_provider.get_current_price(symbol)
            if current_price:
                asset.current_price = current_price
                updated_count += 1

        return updated_count

    def get_portfolio_value(self, portfolio_name):
        """Get the current value of a portfolio."""
        if portfolio_name not in self._portfolios:
            raise ValueError(f"Portfolio '{portfolio_name}' not found")

        portfolio = self._portfolios[portfolio_name]
        return portfolio.total_value()

    def get_portfolio_allocation(self, portfolio_name):
        """Get the asset allocation of a portfolio."""
        if portfolio_name not in self._portfolios:
            raise ValueError(f"Portfolio '{portfolio_name}' not found")

        portfolio = self._portfolios[portfolio_name]
        return portfolio.asset_allocation()

    def create_visualizer(self, portfolio_name):
        """Create a PortfolioVisualizer for a portfolio."""
        if portfolio_name not in self._portfolios:
            raise ValueError(f"Portfolio '{portfolio_name}' not found")

        portfolio = self._portfolios[portfolio_name]
        return PortfolioVisualizer(portfolio, self._data_provider)

    def save_portfolio(self, portfolio_name, file_path):
        """Save a portfolio to a file (simplified example)."""
        if portfolio_name not in self._portfolios:
            raise ValueError(f"Portfolio '{portfolio_name}' not found")

        portfolio = self._portfolios[portfolio_name]

        # In a real application, this would serialize the portfolio to JSON or another format
        # For this example, we'll just print its summary
        with open(file_path, "w") as f:
            f.write(str(portfolio))
            f.write("\n\nHoldings:\n")

            holdings = portfolio.get_holdings()
            for symbol, (asset, quantity) in holdings.items():
                f.write(
                    f"{quantity} shares of {asset.name} ({symbol}) @ ${asset.current_price:.2f}\n"
                )

            f.write(f"\nCash balance: ${portfolio.cash_balance:.2f}\n")
