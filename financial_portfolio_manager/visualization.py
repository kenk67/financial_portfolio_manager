from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd

# Set the style for plots
plt.style.use("ggplot")


class PortfolioVisualizer:
    """Class for generating portfolio visualizations."""

    def __init__(self, portfolio, data_provider):
        self._portfolio = portfolio
        self._data_provider = data_provider

    def plot_portfolio_value_history(self, days=30, save_path=None):
        """
        Plot the historical value of the portfolio over time.

        Args:
            days: Number of days to look back
            save_path: Optional path to save the chart image
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        holdings = self._portfolio.get_holdings()
        dates = [start_date + timedelta(days=i) for i in range(days)]
        total_values = []

        for date in dates:
            total_value = self._portfolio.cash_balance
            for symbol, (asset, quantity) in holdings.items():
                hist_prices = self._data_provider.get_historical_prices(
                    symbol, date, date
                )
                price = hist_prices.get(date, asset.current_price)
                total_value += price * quantity
            total_values.append(total_value)

        fig = plt.figure(figsize=(12, 6))
        plt.plot(dates, total_values, "b-", linewidth=2)
        plt.title(f"Portfolio Value History - Last {days} Days")
        plt.xlabel("Date")
        plt.ylabel("Value ($)")
        plt.grid(True)
        plt.gcf().autofmt_xdate()
        self._add_transaction_markers(dates, total_values)
        if save_path:
            fig.savefig(save_path)
        plt.tight_layout()
        return fig

    def plot_asset_performance(self, days=30, save_path=None):
        """
        Plot the performance of individual assets over time.

        Args:
            days: Number of days to look back
            save_path: Optional path to save the chart image
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        holdings = self._portfolio.get_holdings()
        fig = plt.figure(figsize=(12, 6))

        for symbol, (asset, quantity) in holdings.items():
            hist_prices = self._data_provider.get_historical_prices(
                symbol, start_date, end_date
            )
            if hist_prices:
                sorted_dates = sorted(hist_prices.keys())
                prices = [hist_prices[date] for date in sorted_dates]
                base_price = prices[0] if prices else 1.0
                normalized = [(p / base_price - 1) * 100 for p in prices]
                plt.plot(sorted_dates, normalized, label=f"{asset.name} ({symbol})")

        plt.title(f"Asset Performance - Last {days} Days (% Change)")
        plt.xlabel("Date")
        plt.ylabel("% Change")
        plt.grid(True)
        plt.legend()
        plt.gcf().autofmt_xdate()
        if save_path:
            fig.savefig(save_path)
        plt.tight_layout()
        return fig

    def plot_correlation_matrix(self, days=90, save_path=None):
        """
        Plot a correlation matrix of asset price movements.

        Args:
            days: Number of days to look back for correlation calculation
            save_path: Optional path to save the chart image
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        holdings = self._portfolio.get_holdings()
        symbols = list(holdings.keys())

        if len(symbols) < 2:
            print("Need at least 2 different assets to calculate correlations")
            return None

        price_data = {}
        for symbol in symbols:
            hist_prices = self._data_provider.get_historical_prices(
                symbol, start_date, end_date
            )
            if hist_prices:
                dates = sorted(hist_prices.keys())
                prices = [hist_prices[date] for date in dates]
                price_data[symbol] = pd.Series(prices, index=dates)

        if not price_data:
            return None

        df = pd.DataFrame(price_data)
        returns = df.pct_change().dropna()
        corr_matrix = returns.corr()

        fig = plt.figure(figsize=(10, 8))
        plt.imshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)
        plt.colorbar()
        plt.xticks(range(len(symbols)), symbols, rotation=45)
        plt.yticks(range(len(symbols)), symbols)
        for i in range(len(symbols)):
            for j in range(len(symbols)):
                val = corr_matrix.iloc[i, j]
                plt.text(
                    j,
                    i,
                    f"{val:.2f}",
                    ha="center",
                    va="center",
                    color="black" if abs(val) < 0.5 else "white",
                )
        plt.title("Asset Price Correlation Matrix")
        if save_path:
            fig.savefig(save_path)
        plt.tight_layout()
        return fig

    def plot_asset_allocation(self, save_path=None):
        """
        Plot the portfolio's asset allocation as a pie chart.

        Args:
            save_path: Optional path to save the chart image
        """
        allocation = self._portfolio.asset_allocation()
        labels = list(allocation.keys())
        sizes = list(allocation.values())

        fig = plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.axis("equal")
        plt.title(f"Portfolio Asset Allocation - {self._portfolio.name}")
        if save_path:
            fig.savefig(save_path)
        plt.tight_layout()
        return fig

    def _add_transaction_markers(self, dates, values):
        """Add markers for buy/sell transactions."""
        from .transaction import TransactionType

        transactions = self._portfolio.get_transactions()
        if not dates:
            return
        start_date, end_date = dates[0], dates[-1]
        relevant = [t for t in transactions if start_date <= t.date <= end_date]

        # Buys
        buy_dates = [
            t.date for t in relevant if t.transaction_type == TransactionType.BUY
        ]
        if buy_dates:
            buy_vals = []
            for d in buy_dates:
                idx = min(
                    range(len(dates)), key=lambda i: abs((dates[i] - d).total_seconds())
                )
                buy_vals.append(values[idx])
            plt.plot(buy_dates, buy_vals, "g^", markersize=10, label="Buy")

        # Sells
        sell_dates = [
            t.date for t in relevant if t.transaction_type == TransactionType.SELL
        ]
        if sell_dates:
            sell_vals = []
            for d in sell_dates:
                idx = min(
                    range(len(dates)), key=lambda i: abs((dates[i] - d).total_seconds())
                )
                sell_vals.append(values[idx])
            plt.plot(sell_dates, sell_vals, "rv", markersize=10, label="Sell")

        if buy_dates or sell_dates:
            plt.legend()
