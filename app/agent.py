# app/agent.py
"""Financial Analyst Multi-Agent System Definition.

Orchestrates subagents using ADK Coordinator Pattern, Strategic Model Routing,
History Compaction, Guardrails Plugin, and Human-in-the-Loop portfolio tools.
"""

from google.adk.agents import Agent
from google.adk.agents.context_cache_config import ContextCacheConfig
from google.adk.apps import App, ResumabilityConfig
from google.adk.apps.app import EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.models import Gemini
from google.adk.tools import FunctionTool
from google.genai import types

from app.logger import configure_logging
from app.memory import generate_memories_callback, get_preload_memory_tool
from app.plugins import FinancialPolicyPlugin
from app.tools import (
    correlate_news_with_market_metrics,
    extract_financial_news_signals,
    fetch_income_statement_metrics,
    fetch_realtime_stock_quote,
    save_user_portfolio_allocation,
)

# Configure structured JSON logging
configure_logging("INFO")

# Define Strategic Models
FLASH_MODEL = "gemini-2.5-flash"
PRO_MODEL = "gemini-2.5-pro"

# System Constitution
FINANCIAL_ANALYST_CONSTITUTION = """
You are the Lead Financial Data & Investment Analyst Agent.

CONSTITUTION & CORE DIRECTIVES:
1. PURPOSE: Fetch market metrics, analyze fundamental income statements, extract critical news,
   and establish causal connections between market events and company financials.
2. DOMAIN BOUNDARIES: Respond strictly to financial, market, stock, corporate earnings, and investment queries.
   Politely decline non-financial topics.
3. VERIFICATION & CITATION: Always cite specific ticker symbols, prices, P/E ratios, and news headlines.
   Do not make up financial statistics.
4. ACTIONABLE OUTPUT: Format financial reports using Markdown tables, bullet points, and clear sentiment summaries.
5. REQUIRED DISCLAIMER: End every overall response with an explicit financial disclaimer:
   "Not financial advice. For informational purposes only."
"""

# Subagent 1: Market Data Specialist (Fast Model: Flash)
market_data_agent = Agent(
    name="market_data_specialist",
    model=Gemini(model=FLASH_MODEL),
    instruction=(
        "You are a market data specialist. Your role is to fetch real-time stock quotes, "
        "P/E ratios, trading volumes, and income statement financial metrics using your tools."
    ),
    description="Fetches real-time stock prices, volume, market cap, and income statements.",
    tools=[fetch_realtime_stock_quote, fetch_income_statement_metrics],
)

# Subagent 2: News & Sentiment Analyst (Fast Model: Flash)
news_analysis_agent = Agent(
    name="news_analysis_specialist",
    model=Gemini(model=FLASH_MODEL),
    instruction=(
        "You are a financial news specialist. Extract key headlines, publishers, and publication "
        "dates for target stock tickers to highlight market catalysts."
    ),
    description="Retrieves and extracts recent financial news headlines and press releases.",
    tools=[extract_financial_news_signals],
)

# Subagent 3: Connection & Causal Synthesizer (Reasoning Model: Pro)
connection_synthesizer_agent = Agent(
    name="connection_synthesizer_specialist",
    model=Gemini(model=PRO_MODEL),
    instruction=(
        "You are a senior investment strategist. Analyze news signals alongside company metrics "
        "to synthesize causal narratives, evaluate market sentiment, and explain how external news impacts performance."
    ),
    description="Correlates news headlines with fundamental metrics to build investment narratives.",
    tools=[correlate_news_with_market_metrics],
)

# Human-in-the-loop Portfolio Allocation Tool
portfolio_tool = FunctionTool(
    save_user_portfolio_allocation,
    require_confirmation=True,  # Explicit HITL Code Stop
)

# Root Coordinator Agent (Reasoning Model: Pro)
root_agent = Agent(
    name="financial_coordinator",
    model=Gemini(
        model=PRO_MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=FINANCIAL_ANALYST_CONSTITUTION,
    description="Root coordinator for financial queries, investment analysis, and market Q&A.",
    sub_agents=[
        market_data_agent,
        news_analysis_agent,
        connection_synthesizer_agent,
    ],
    tools=[
        get_preload_memory_tool(),
        fetch_realtime_stock_quote,
        fetch_income_statement_metrics,
        extract_financial_news_signals,
        correlate_news_with_market_metrics,
        portfolio_tool,
    ],
    after_agent_callback=generate_memories_callback,
)

# Configure ADK Application with Compaction, Resumability, and Guardrail Plugins
app = App(
    name="app",  # Must match the directory name 'app'
    root_agent=root_agent,
    plugins=[FinancialPolicyPlugin()],
    resumability_config=ResumabilityConfig(is_resumable=True),
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=15,
        overlap_size=3,
        summarizer=LlmEventSummarizer(llm=Gemini(model=FLASH_MODEL)),
    ),
    context_cache_config=ContextCacheConfig(
        min_tokens=2048,
        ttl_seconds=1800,
    ),
)
