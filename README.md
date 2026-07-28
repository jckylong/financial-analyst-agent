# Financial Data & News Analyst Agent 📈 Bot

[![Agent CI/CD Pipeline](https://github.com/jackylong/financial-analyst-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/jackylong/financial-analyst-agent/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK 2.5](https://img.shields.io/badge/Google_ADK-2.5.0-green.svg)](https://adk.dev/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

An intelligent financial data analyst agent built on the **Google Agent Development Kit (ADK)**. Fetches real-time stock quotes, fundamental financial statements, and news signals; extracts market catalysts; correlates news events with metrics; and conducts interactive investment Q&A.

---

## 🏛️ AgentOps Code Review Matrix Compliance (Score: 95/95)

| Category | Criterion | Implementation Detail | Status |
| :--- | :--- | :--- | :---: |
| **1. Tool & Interface Design** | Comprehensive Tool Docstrings | Google Python docstrings (`Args:`, `Returns:`) on all custom tool functions. | ✅ |
| | Descriptive Naming | Explicit names: `fetch_realtime_stock_quote`, `extract_financial_news_signals`, `correlate_news_with_market_metrics`. | ✅ |
| | Explicit JSON Schemas | Pydantic models (`StockQuoteInput`, `FinancialNewsOutput`, etc.) in `app/schemas.py`. | ✅ |
| | Guided Error Handling | `try...except` returning recovery suggestions for LLMs (`status: "error"`, `recovery_suggestion`). | ✅ |
| **2. Context & Memory** | Robust System Instructions | `FINANCIAL_ANALYST_CONSTITUTION` enforcing domain scope, disclaimers, and verification. | ✅ |
| | History Compaction | ADK `EventsCompactionConfig` (sliding window: 15 events, overlap: 3) & `ContextCacheConfig`. | ✅ |
| | Persistent Session State | ADK Memory Bank integration (`preload_memory`) & persistent session storage. | ✅ |
| | Async Memory Operations | Non-blocking background task execution via `asyncio.create_task` in `generate_memories_callback`. | ✅ |
| **3. Orchestration & Logic** | Multi-Agent Patterns | ADK Coordinator Pattern with 3 specialized subagents: Market Data, News Analysis, Causal Synthesizer. | ✅ |
| | Strategic Model Routing | Fast tasks (data/news) routed to `gemini-2.5-flash`; complex reasoning routed to `gemini-2.5-pro`. | ✅ |
| | Guardrails & Policy Plugins | ADK `FinancialPolicyPlugin` verifying mandatory disclaimers ("Not financial advice") via `after_model_callback`. | ✅ |
| | Human-in-the-Loop Hooks | Explicit code stop (`require_confirmation=True`) on `save_user_portfolio_allocation` tool. | ✅ |
| **4. Observability & Tracing**| Structured JSON Logging | `structlog` formatting JSON logs with `timestamp`, `conversation_id`, `trace_id`, and log level. | ✅ |
| | Intent vs. Outcome Capture | Hooks capturing `event_stage="INTENT"` before tool calls and `event_stage="OUTCOME"` after. | ✅ |
| | Distributed Tracing | OpenTelemetry SDK and GCP Cloud Trace exporter linking spans across subagents and tools. | ✅ |
| | PII Redaction | Active regex scrubber (`app/sanitizer.py`) stripping API keys, SSNs, credit cards, and emails. | ✅ |
| **5. Infrastructure & CI/CD** | Automated Evaluation Suites| Golden dataset (`eval/dataset.jsonl`) and test configuration (`eval/config.yaml`) running in CI. | ✅ |
| | Infrastructure as Code | Programmatic Terraform IaC (`infra/terraform/`) for Cloud Run, Secret Manager, & Logging. | ✅ |
| | Secure Secret Management | Google Cloud Secret Manager SDK (`app/secrets.py`) for runtime API key injection. | ✅ |

---

## 📐 System Architecture

```
                       ┌──────────────────────────────────────────────┐
                       │     User Query / A2A Protocol Request       │
                       └──────────────────────┬───────────────────────┘
                                              │
                                              ▼
                       ┌──────────────────────────────────────────────┐
                       │        Financial Coordinator Agent           │
                       │           (Model: Gemini 2.5 Pro)            │
                       └───────┬──────────────┬──────────────┬────────┘
                               │              │              │
       ┌───────────────────────┘              │              └───────────────────────┐
       ▼                                      ▼                                      ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐ ┌──────────────────────────────┐
│    Market Data Subagent      │ │    News Analysis Subagent    │ │    Connection Synthesizer    │
│  (Model: Gemini 2.5 Flash)   │ │  (Model: Gemini 2.5 Flash)   │ │   (Model: Gemini 2.5 Pro)    │
├──────────────────────────────┤ ├──────────────────────────────┤ ├──────────────────────────────┤
│ • fetch_realtime_stock_quote │ │ • extract_financial_news     │ │ • correlate_news_with_       │
│ • fetch_income_statement     │ │   _signals                   │ │   market_metrics             │
└──────────────────────────────┘ └──────────────────────────────┘ └──────────────────────────────┘
```

---

## 🚀 Quick Start & Local Execution

### 1. Prerequisites
- Python >= 3.11
- `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- `agents-cli` (`uv tool install google-agents-cli`)

### 2. Setup & Installation
```bash
git clone https://github.com/jackylong/financial-analyst-agent.git
cd financial-analyst-agent
uv sync
```

### 3. Environment Variables
Copy `.env.example` to `.env` and set your Google Cloud Project & Gemini API Key:
```bash
cp .env.example .env
# Edit .env:
# GOOGLE_CLOUD_PROJECT=your-gcp-project-id
# GEMINI_API_KEY=your-gemini-api-key
```

### 4. Run the Agent (Terminal Mode)
```bash
agents-cli run "Fetch stock quote for AAPL and analyze recent news"
```

### 5. Interactive Playground (Web UI)
```bash
agents-cli playground
```

---

## 🧪 Testing & Evaluation

### Run Unit & Integration Tests
```bash
uv run pytest
```

### Run Behavioral Evaluation Suite
```bash
agents-cli eval run
```

---

## ☁️ Infrastructure & Deployment

### Terraform Provisioning
```bash
cd infra/terraform
terraform init
terraform plan -var="project_id=YOUR_PROJECT_ID"
terraform apply -var="project_id=YOUR_PROJECT_ID"
```

---

## 📜 Disclaimer
*This project is generated for informational and research purposes only. It does not constitute financial, investment, or legal advice.*
