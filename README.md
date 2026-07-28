# Financial Data & News Analyst Agent 📈 Bot

[![Agent CI/CD Pipeline](https://github.com/jckylong/financial-analyst-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/jckylong/financial-analyst-agent/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK 2.5](https://img.shields.io/badge/Google_ADK-2.5.0-green.svg)](https://adk.dev/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

An intelligent financial data analyst agent built on the **Google Agent Development Kit (ADK)**. Fetches real-time stock quotes, fundamental financial statements, and news signals; extracts market catalysts; correlates news events with metrics; and conducts interactive investment Q&A.

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
git clone https://github.com/jckylong/financial-analyst-agent.git
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

## 🧪 Testing

### Run Unit & Integration Tests
```bash
uv run pytest
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
