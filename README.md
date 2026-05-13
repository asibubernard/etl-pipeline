# 🔁 Ghana Financial Data ETL Pipeline

A production-style Extract-Transform-Load (ETL) pipeline that ingests Ghana macrofinancial data from the **World Bank API**, applies data quality transformations, runs validation checks, and loads into a **SQLite data warehouse** — with a Flask web UI to trigger and monitor runs.

**Live Demo:** [your-app.onrender.com](#) &nbsp;|&nbsp; **Portfolio:** [linkedin.com/in/asibubernard](https://linkedin.com/in/asibubernard)

---

## 🏗 Pipeline Architecture

```
World Bank API
     │
     ▼
[EXTRACT]  → 8 macroeconomic indicators · 24 years (2000–2023)
     │
     ▼
[TRANSFORM] → Missing value imputation · Derived columns
              Inflation bands · Debt sustainability flags
              FX YoY change · Real GDP proxy
     │
     ▼
[VALIDATE]  → 6 data quality checks (nulls, ranges, duplicates)
     │
     ▼
[LOAD]      → SQLite: 3 tables
              ghana_macro_indicators · macro_summary · yearly_changes
     │
     ▼
Flask Dashboard → Live charts · Data table · Pipeline log
```

## 📊 Indicators Extracted

| World Bank Code | Metric |
|-----------------|--------|
| FP.CPI.TOTL.ZG | Inflation rate (%) |
| NY.GDP.MKTP.KD.ZG | GDP growth rate (%) |
| PA.NUS.FCRF | Official exchange rate (USD/GHS) |
| FS.AST.PRVT.GD.ZS | Private credit (% GDP) |
| GC.DOD.TOTL.GD.ZS | Central govt debt (% GDP) |
| BN.CAB.XOKA.GD.ZS | Current account balance (% GDP) |
| NE.TRD.GNFS.ZS | Trade openness (% GDP) |
| SL.UEM.TOTL.ZS | Unemployment rate (%) |

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| ETL Engine | Python · Pandas · Requests |
| Database | SQLite (3 tables) |
| Web UI | Flask · Plotly.js |
| Logging | Python logging module |
| Deployment | Render / Railway |

## 🚀 Run Locally

```bash
git clone https://github.com/asibubernard/ghana-etl-pipeline
cd ghana-etl-pipeline
pip install -r requirements.txt

# Run pipeline directly
python etl_pipeline.py

# Or launch the web dashboard
python app.py   # → http://localhost:5001
```

## 🗄 SQL Analysis

See `sql/analysis_queries.sql` for 8 ready-to-run analytical queries including:
- Decade-by-decade averages
- High inflation episode identification
- Debt sustainability classification
- FX regime analysis

## 📂 Project Structure

```
project2-etl-pipeline/
├── etl_pipeline.py         # Core ETL logic (extract/transform/validate/load)
├── app.py                  # Flask dashboard
├── requirements.txt
├── data/
│   ├── ghana_finance.db    # SQLite output (generated)
│   └── etl.log             # Run log
├── sql/
│   └── analysis_queries.sql
└── templates/
    └── index.html
```
