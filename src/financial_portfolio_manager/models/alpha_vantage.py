from datetime import date
from typing import Dict

from pydantic import BaseModel, Field


class GlobalQuote(BaseModel):
    symbol: str = Field(alias="01. symbol")
    open: float = Field(alias="02. open")
    high: float = Field(alias="03. high")
    low: float = Field(alias="04. low")
    price: float = Field(alias="05. price")
    volume: int = Field(alias="06. volume")
    latest_trading_day: str = Field(alias="07. latest trading day")
    previous_close: float = Field(alias="08. previous close")
    change: float = Field(alias="09. change")
    change_percent: str = Field(alias="10. change percent")


class AlphaVantageQuoteResponse(BaseModel):
    global_quote: GlobalQuote = Field(alias="Global Quote")


class DailyPrice(BaseModel):
    open: float = Field(alias="1. open")
    high: float = Field(alias="2. high")
    low: float = Field(alias="3. low")
    close: float = Field(alias="4. close")
    volume: int = Field(alias="5. volume")


class MetaData(BaseModel):
    information: str = Field(alias="1. Information")
    symbol: str = Field(alias="2. Symbol")
    last_refreshed: date = Field(alias="3. Last Refreshed")
    output_size: str = Field(alias="4. Output Size")
    time_zone: str = Field(alias="5. Time Zone")


class AlphaVantageTimeSeriesDaily(BaseModel):
    meta_data: MetaData = Field(alias="Meta Data")
    time_series: Dict[date, DailyPrice] = Field(alias="Time Series (Daily)")


class CompanyOverview(BaseModel):
    symbol: str = Field(alias="Symbol")
    asset_type: str = Field(alias="AssetType")
    name: str = Field(alias="Name")
    description: str = Field(alias="Description")
    cik: str = Field(alias="CIK")
    exchange: str = Field(alias="Exchange")
    currency: str = Field(alias="Currency")
    country: str = Field(alias="Country")
    sector: str = Field(alias="Sector")
    industry: str = Field(alias="Industry")
    address: str = Field(alias="Address")
    official_site: str = Field(alias="OfficialSite")
    fiscal_year_end: str = Field(alias="FiscalYearEnd")
    latest_quarter: str = Field(alias="LatestQuarter")
    market_capitalization: str = Field(alias="MarketCapitalization")
    ebitda: str = Field(alias="EBITDA")
    pe_ratio: str = Field(alias="PERatio")
    peg_ratio: str = Field(alias="PEGRatio")
    book_value: str = Field(alias="BookValue")
    dividend_per_share: str = Field(alias="DividendPerShare")
    dividend_yield: str = Field(alias="DividendYield")
    eps: str = Field(alias="EPS")
    revenue_per_share_ttm: str = Field(alias="RevenuePerShareTTM")
    profit_margin: str = Field(alias="ProfitMargin")
    operating_margin_ttm: str = Field(alias="OperatingMarginTTM")
    return_on_assets_ttm: str = Field(alias="ReturnOnAssetsTTM")
    return_on_equity_ttm: str = Field(alias="ReturnOnEquityTTM")
    revenue_ttm: str = Field(alias="RevenueTTM")
    gross_profit_ttm: str = Field(alias="GrossProfitTTM")
    diluted_eps_ttm: str = Field(alias="DilutedEPSTTM")
    quarterly_earnings_growth_yoy: str = Field(alias="QuarterlyEarningsGrowthYOY")
    quarterly_revenue_growth_yoy: str = Field(alias="QuarterlyRevenueGrowthYOY")
    analyst_target_price: str = Field(alias="AnalystTargetPrice")
    analyst_rating_strong_buy: str = Field(alias="AnalystRatingStrongBuy")
    analyst_rating_buy: str = Field(alias="AnalystRatingBuy")
    analyst_rating_hold: str = Field(alias="AnalystRatingHold")
    analyst_rating_sell: str = Field(alias="AnalystRatingSell")
    analyst_rating_strong_sell: str = Field(alias="AnalystRatingStrongSell")
    trailing_pe: str = Field(alias="TrailingPE")
    forward_pe: str = Field(alias="ForwardPE")
    price_to_sales_ratio_ttm: str = Field(alias="PriceToSalesRatioTTM")
    price_to_book_ratio: str = Field(alias="PriceToBookRatio")
    ev_to_revenue: str = Field(alias="EVToRevenue")
    ev_to_ebitda: str = Field(alias="EVToEBITDA")
    beta: str = Field(alias="Beta")
    week_52_high: str = Field(alias="52WeekHigh")
    week_52_low: str = Field(alias="52WeekLow")
    day_50_moving_average: str = Field(alias="50DayMovingAverage")
    day_200_moving_average: str = Field(alias="200DayMovingAverage")
    shares_outstanding: str = Field(alias="SharesOutstanding")
    dividend_date: str = Field(alias="DividendDate")
    ex_dividend_date: str = Field(alias="ExDividendDate")
