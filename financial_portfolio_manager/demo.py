#!/usr/bin/env python3
"""
Demo script showing usage of the Financial Portfolio Manager.
"""

import os
import sys
from datetime import datetime, timedelta

import matplotlib.pyplot as plt

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our main application
from financial_portfolio_manager.main import FinancialPortfolioManager


def main():
    """Run the demo."""
    print("Financial Portfolio Manager Demo")
    print("================================")

    # Create the application using the mock data provider
    app = FinancialPortfolioManager(data_provider_type="mock")

    # Create a portfolio
    portfolio_name = "Demo Portfolio"
    print(f"\nCreating portfolio: {portfolio_name}")
    portfolio = app.create_portfolio(portfolio_name, "John Doe")

    # Deposit initial cash
    initial_deposit = 10000.0
    print(f"Depositing ${initial_deposit:.2f}")
    app.deposit_cash(portfolio_name, initial_deposit)

    # Create and buy some assets
    print("\nBuying assets:")

    # Buy Apple stock
    apple_stock = app.create_stock("AAPL", "Apple Inc.")
    quantity = 10
    print(
        f"  - Buying {quantity} shares of {apple_stock.name} @ ${apple_stock.current_price:.2f}"
    )
    app.buy_asset(portfolio_name, apple_stock, quantity)

    # Buy Microsoft stock
    msft_stock = app.create_stock("MSFT", "Microsoft Corp.")
    quantity = 5
    print(
        f"  - Buying {quantity} shares of {msft_stock.name} @ ${msft_stock.current_price:.2f}"
    )
    app.buy_asset(portfolio_name, msft_stock, quantity)

    # Buy Amazon stock
    amzn_stock = app.create_stock("AMZN", "Amazon.com Inc.")
    quantity = 3
    print(
        f"  - Buying {quantity} shares of {amzn_stock.name} @ ${amzn_stock.current_price:.2f}"
    )
    app.buy_asset(portfolio_name, amzn_stock, quantity)

    # Create a bond with hypothetical data
    maturity_date = datetime.now() + timedelta(days=365 * 5)  # 5 years from now
    bond = app.create_bond(
        symbol="T5Y",
        name="5-Year Treasury",
        face_value=1000.0,
        coupon_rate=0.025,  # 2.5%
        maturity_date=maturity_date,
    )
    quantity = 5
    print(f"  - Buying {quantity} of {bond.name} @ ${bond.current_price:.2f}")
    app.buy_asset(portfolio_name, bond, quantity)

    # Display portfolio summary
    print("\nPortfolio Summary:")
    value = app.get_portfolio_value(portfolio_name)
    print(f"Total value: ${value:.2f}")

    # Display asset allocation
    allocation = app.get_portfolio_allocation(portfolio_name)
    print("\nAsset Allocation:")
    for asset_type, percentage in allocation.items():
        print(f"  - {asset_type.capitalize()}: {percentage:.1f}%")

    # Create visualizations
    print("\nCreating visualizations...")
    visualizer = app.create_visualizer(portfolio_name)

    # Plot portfolio value history
    print("  - Portfolio value history")
    fig = visualizer.plot_portfolio_value_history(days=30)
    plt.savefig("portfolio_value_history.png")

    # Plot asset allocation
    print("  - Asset allocation")
    fig = visualizer.plot_asset_allocation()
    plt.savefig("asset_allocation.png")

    # Plot asset performance comparison
    print("  - Asset performance")
    fig = visualizer.plot_asset_performance(days=30)
    plt.savefig("asset_performance.png")

    # Plot correlation matrix
    print("  - Asset correlation matrix")
    fig = visualizer.plot_correlation_matrix()
    plt.savefig("correlation_matrix.png")

    # Sell some assets
    print("\nSelling assets:")
    quantity = 2
    print(f"  - Selling {quantity} shares of {apple_stock.name}")
    app.sell_asset(portfolio_name, "AAPL", quantity)

    # Final portfolio summary
    print("\nFinal Portfolio Summary:")
    value = app.get_portfolio_value(portfolio_name)
    print(f"Total value: ${value:.2f}")

    # Save portfolio to file
    output_file = "portfolio_summary.txt"
    print(f"\nSaving portfolio to {output_file}")
    app.save_portfolio(portfolio_name, output_file)

    print("\nDemo completed successfully!")
    print(f"Check the generated files in the current directory.")


if __name__ == "__main__":
    main()
