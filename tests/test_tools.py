# tests/test_tools.py
"""Unit tests for financial data retrieval and analysis tools."""

from app.tools import (
    correlate_news_with_market_metrics,
    extract_financial_news_signals,
    fetch_income_statement_metrics,
    fetch_realtime_stock_quote,
    save_user_portfolio_allocation,
)


def test_fetch_realtime_stock_quote_valid():
    """Test fetch_realtime_stock_quote with a standard valid symbol."""
    res = fetch_realtime_stock_quote("AAPL")
    assert "status" in res
    assert res["symbol"] == "AAPL"
    if res["status"] == "success":
        assert "current_price" in res
        assert isinstance(res["current_price"], float)


def test_fetch_realtime_stock_quote_invalid():
    """Test guided error handling when ticker symbol is invalid."""
    res = fetch_realtime_stock_quote("INVALIDTICKERXYZ123")
    assert res["status"] == "error"
    assert "recovery_suggestion" in res
    assert "Verify" in res["recovery_suggestion"] or "exchange" in res["recovery_suggestion"]


def test_fetch_income_statement_metrics():
    """Test fetching income statement metrics."""
    res = fetch_income_statement_metrics("MSFT")
    assert "status" in res
    assert res["symbol"] == "MSFT"


def test_extract_financial_news_signals():
    """Test news extraction tool."""
    res = extract_financial_news_signals("GOOGL", limit=3)
    assert res["status"] == "success"
    assert "articles" in res
    assert isinstance(res["articles"], list)


def test_correlate_news_with_market_metrics():
    """Test news-metric correlation tool."""
    res = correlate_news_with_market_metrics(
        symbol="NVDA",
        news_headlines=["NVIDIA announces strong AI chip demand"],
        key_metrics_summary="Price: $120, P/E: 45",
    )
    assert res["status"] == "success"
    assert res["symbol"] == "NVDA"
    assert "impact_narrative" in res


def test_save_user_portfolio_allocation():
    """Test HITL portfolio allocation tool."""
    res = save_user_portfolio_allocation(
        symbol="AAPL",
        target_allocation_pct=15.0,
        conviction_level="High",
    )
    assert res["symbol"] == "AAPL"
    assert res["target_allocation_pct"] == 15.0
    assert res["confirmation_status"] == "APPROVED"
