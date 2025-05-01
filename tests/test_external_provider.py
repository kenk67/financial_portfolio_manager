from datetime import date, timedelta

import pytest

from src.financial_portfolio_manager.external_data_provider.alpha_vantage_provider import (
    AlphaVantageProvider,
)


@pytest.fixture
def alphavantage_provider():
    """Fixture for AlphaVantageProvider."""
    return AlphaVantageProvider()


def test_alpha_vantage_provider_get_api(alphavantage_provider):
    function = "GLOBAL_QUOTE"
    symbol = "IBM"

    response = alphavantage_provider.get_api_data(function=function, symbol=symbol)
    assert isinstance(response, dict)


def test_alpha_vantage_provider_get_current_price(alphavantage_provider):
    symbol = "IBM"

    price = alphavantage_provider.get_current_price(symbol=symbol)
    assert isinstance(price, float)


def test_alpha_vantage_provider_get_historical_prices(alphavantage_provider):
    symbol = "IBM"
    start_date = date.today() - timedelta(days=10)
    end_date = start_date - timedelta(days=30)

    historical_prices = alphavantage_provider.get_historical_prices(
        symbol=symbol, start_date=start_date, end_date=end_date
    )
    assert isinstance(historical_prices, dict)


def test_alpha_vantage_provider_get_company_info(alphavantage_provider):
    symbol = "IBM"

    company_overview = alphavantage_provider.get_company_info(symbol=symbol)
    assert isinstance(company_overview, dict)
    assert "Name" in company_overview
    assert "Description" in company_overview
    assert "Sector" in company_overview
