# app/schemas.py
"""Pydantic schemas for tool inputs, outputs, and financial data structures.

Enforces strict JSON schema validation for LLM tool calling.
"""

from pydantic import BaseModel, Field


class StockQuoteInput(BaseModel):
    """Input schema for fetching real-time stock quote."""

    symbol: str = Field(
        ...,
        description="The stock ticker symbol, e.g., 'AAPL', 'MSFT', 'GOOGL'. Must be uppercase.",
    )


class StockQuoteOutput(BaseModel):
    """Output schema for real-time stock quote response."""

    symbol: str = Field(..., description="Stock ticker symbol.")
    company_name: str = Field(..., description="Full company name.")
    current_price: float = Field(..., description="Current stock price in USD.")
    day_high: float = Field(..., description="High price for current trading day.")
    day_low: float = Field(..., description="Low price for current trading day.")
    volume: int = Field(..., description="Trading volume for current day.")
    market_cap: int | float = Field(..., description="Total market capitalization in USD.")
    pe_ratio: float | None = Field(None, description="Trailing Price-to-Earnings ratio.")
    eps: float | None = Field(None, description="Earnings per share.")
    fifty_two_week_high: float = Field(..., description="52-week high price.")
    fifty_two_week_low: float = Field(..., description="52-week low price.")
    status: str = Field("success", description="Status of the tool call ('success' or 'error').")
    error_message: str | None = Field(None, description="Detailed error message if failed.")
    recovery_suggestion: str | None = Field(
        None, description="Instructions for LLM to recover from error."
    )


class IncomeStatementInput(BaseModel):
    """Input schema for fetching company financial statements."""

    symbol: str = Field(
        ...,
        description="The stock ticker symbol, e.g., 'NVDA', 'AMZN'. Must be uppercase.",
    )


class IncomeStatementOutput(BaseModel):
    """Output schema for financial income statement metrics."""

    symbol: str = Field(..., description="Stock ticker symbol.")
    total_revenue: int | float | None = Field(None, description="Total revenue for past fiscal year.")
    net_income: int | float | None = Field(None, description="Net income for past fiscal year.")
    gross_profit: int | float | None = Field(None, description="Gross profit for past fiscal year.")
    operating_margin: float | None = Field(None, description="Operating margin percentage.")
    status: str = Field("success", description="Status of the tool execution.")
    error_message: str | None = Field(None, description="Error message if operation failed.")
    recovery_suggestion: str | None = Field(
        None, description="Instructions for LLM to recover from error."
    )


class FinancialNewsInput(BaseModel):
    """Input schema for searching and extracting financial news."""

    symbol: str = Field(
        ...,
        description="The stock ticker symbol to query news for, e.g., 'TSLA'.",
    )
    limit: int = Field(
        5,
        description="Maximum number of news articles to retrieve (1-10).",
    )


class NewsArticle(BaseModel):
    """Structured representation of a financial news article."""

    title: str = Field(..., description="Article headline title.")
    publisher: str = Field(..., description="Publishing outlet or news agency.")
    link: str = Field(..., description="Direct link or reference URL.")
    publish_time: str = Field(..., description="Publication timestamp or date string.")
    summary: str = Field(..., description="Brief summary of article content.")


class FinancialNewsOutput(BaseModel):
    """Output schema for financial news extraction."""

    symbol: str = Field(..., description="Stock ticker symbol.")
    article_count: int = Field(..., description="Number of news articles returned.")
    articles: list[NewsArticle] = Field(default_factory=list, description="List of structured news items.")
    status: str = Field("success", description="Status of news extraction.")
    error_message: str | None = Field(None, description="Error message if news retrieval failed.")
    recovery_suggestion: str | None = Field(
        None, description="Instructions for LLM to recover from error."
    )


class ConnectionAnalysisInput(BaseModel):
    """Input schema for correlating news events with financial performance metrics."""

    symbol: str = Field(..., description="Target stock ticker symbol.")
    news_headlines: list[str] = Field(..., description="List of recent news headlines or summaries.")
    key_metrics_summary: str = Field(
        ..., description="Summary string of current price, P/E, revenue growth, or guidance."
    )


class ConnectionAnalysisOutput(BaseModel):
    """Output schema for news-metric correlation analysis."""

    symbol: str = Field(..., description="Stock ticker symbol.")
    key_catalysts: list[str] = Field(..., description="List of identified market catalysts.")
    sentiment_score: str = Field(
        ..., description="Overall market sentiment: Bullish, Bearish, or Neutral."
    )
    impact_narrative: str = Field(
        ..., description="Synthesized narrative connecting news events to metrics."
    )
    status: str = Field("success", description="Status of correlation synthesis.")


class PortfolioAllocationInput(BaseModel):
    """Input schema for saving/updating portfolio watchlist allocation (Human-in-the-Loop)."""

    symbol: str = Field(..., description="Stock ticker symbol to add or modify.")
    target_allocation_pct: float = Field(
        ..., description="Target allocation percentage in portfolio (0.0 to 100.0)."
    )
    conviction_level: str = Field(
        ..., description="Conviction rating: 'High', 'Medium', or 'Low'."
    )


class PortfolioAllocationOutput(BaseModel):
    """Output schema for portfolio allocation update."""

    symbol: str = Field(..., description="Updated stock ticker symbol.")
    target_allocation_pct: float = Field(..., description="Target allocation percentage.")
    confirmation_status: str = Field(
        "APPROVED", description="Confirmation status: 'APPROVED' or 'PENDING_HUMAN_APPROVAL'."
    )
    message: str = Field(..., description="Human-readable result message.")
