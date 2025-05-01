# Financial Portfolio Manager

A Python-based financial portfolio management system for tracking investments, analyzing performance, and visualizing financial data.

## Features

- Track multiple investment portfolios
- Support for different asset types (stocks, bonds)
- Real-time market data integration (via external APIs)
- Transaction history tracking 
- Portfolio performance visualization
- Asset allocation analysis
- Correlation analysis between assets

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/financial_portfolio_manager.git
cd financial_portfolio_manager

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package and dependencies
pip install -e .
```

## Usage

Here's a basic example to get started:

```python
from portfolio_manager.main import FinancialPortfolioManager

# Create the portfolio manager (using mock data for testing)
app = FinancialPortfolioManager(data_provider_type="mock")

# Create a portfolio
portfolio = app.create_portfolio("My Portfolio", "John Doe")

# Add initial cash
app.deposit_cash("My Portfolio", 10000.0)

# Create and buy assets
apple_stock = app.create_stock("AAPL", "Apple Inc.")
app.buy_asset("My Portfolio", apple_stock, 10)

# Check portfolio value
value = app.get_portfolio_value("My Portfolio")
print(f"Portfolio value: ${value:.2f}")

# Create visualizations
visualizer = app.create_visualizer("My Portfolio")
fig = visualizer.plot_portfolio_value_history()
fig.savefig("portfolio_history.png")
```

For more detailed examples, check the `examples` directory.

## Object-Oriented Programming Concepts

This project demonstrates several key OOP concepts:

### Encapsulation

- Private attributes with getter/setter methods
- Data validation within setters 
- Information hiding through property decorators

### Aggregation/Composition

- Portfolio aggregates Assets and Transactions
- Broker uses but doesn't own Portfolios

### SOLID Principles

1. **Single Responsibility Principle**
   - Each class has one responsibility (e.g., Asset manages asset data, Portfolio manages holdings)

2. **Open/Closed Principle**
   - Classes are open for extension but closed for modification (e.g., Stock and Bond extend Asset)

3. **Liskov Substitution Principle**
   - Derived classes can be substituted for their base classes (e.g., Stock can be used wherever Asset is expected)

4. **Interface Segregation Principle**
   - Clients aren't forced to depend on methods they don't use (e.g., DataProviderInterface)

5. **Dependency Inversion Principle**
   - High-level modules depend on abstractions, not concrete implementations (e.g., Broker depends on interfaces)

## Requirements

- Python 3.6 or higher
- External libraries: requests, matplotlib, numpy, pandas

## Testing

Run the tests with pytest:

```bash
pytest
```

## License

MIT License - see LICENSE file for details.