-- ============================================================
-- Ghana Financial Data ETL Pipeline — SQL Analysis Queries
-- Author: Bernard Asibu | Data Analytics Portfolio
-- Database: ghana_finance.db (SQLite)
-- ============================================================


-- ── 1. FULL MACRO SUMMARY ─────────────────────────────────────────────
SELECT
    year,
    inflation_pct,
    gdp_growth_pct,
    ROUND(official_fx_rate, 2)          AS usd_ghs_rate,
    central_govt_debt_pct_gdp           AS govt_debt_pct_gdp,
    inflation_band,
    debt_sustainability
FROM ghana_macro_indicators
ORDER BY year DESC;


-- ── 2. DECADES AVERAGE COMPARISON ────────────────────────────────────
SELECT
    CASE
        WHEN year BETWEEN 2000 AND 2009 THEN '2000s'
        WHEN year BETWEEN 2010 AND 2019 THEN '2010s'
        ELSE '2020s'
    END AS decade,
    ROUND(AVG(inflation_pct), 2)             AS avg_inflation,
    ROUND(AVG(gdp_growth_pct), 2)            AS avg_gdp_growth,
    ROUND(AVG(official_fx_rate), 2)          AS avg_usd_ghs,
    ROUND(AVG(central_govt_debt_pct_gdp), 1) AS avg_debt_pct_gdp
FROM ghana_macro_indicators
GROUP BY decade
ORDER BY decade;


-- ── 3. HIGH INFLATION EPISODES (>20%) ─────────────────────────────────
SELECT
    year,
    inflation_pct,
    gdp_growth_pct,
    official_fx_rate,
    real_gdp_proxy  AS real_gdp_approx
FROM ghana_macro_indicators
WHERE inflation_pct > 20
ORDER BY inflation_pct DESC;


-- ── 4. YEAR-ON-YEAR CHANGES ──────────────────────────────────────────
SELECT
    year,
    inflation_pct,
    ROUND(inflation_pct_yoy, 2)      AS inflation_change,
    gdp_growth_pct,
    ROUND(gdp_growth_pct_yoy, 2)     AS gdp_change,
    official_fx_rate,
    ROUND(official_fx_rate_yoy, 2)   AS fx_change
FROM yearly_changes
ORDER BY year DESC
LIMIT 10;


-- ── 5. DEBT SUSTAINABILITY BREAKDOWN ────────────────────────────────
SELECT
    debt_sustainability,
    COUNT(*) AS years_count,
    ROUND(AVG(gdp_growth_pct), 2) AS avg_gdp_growth,
    ROUND(AVG(inflation_pct), 2)  AS avg_inflation
FROM ghana_macro_indicators
GROUP BY debt_sustainability
ORDER BY years_count DESC;


-- ── 6. CORRELATION PROXY: Inflation vs FX Depreciation ──────────────
SELECT
    year,
    inflation_pct,
    fx_yoy_change_pct,
    CASE
        WHEN fx_yoy_change_pct > 15 THEN 'Sharp Depreciation'
        WHEN fx_yoy_change_pct > 5  THEN 'Moderate Depreciation'
        WHEN fx_yoy_change_pct >= 0 THEN 'Stable/Mild'
        ELSE 'Appreciation'
    END AS fx_regime
FROM ghana_macro_indicators
WHERE fx_yoy_change_pct IS NOT NULL
ORDER BY year;


-- ── 7. BEST & WORST YEARS BY GDP GROWTH ──────────────────────────────
(SELECT 'Top 5' AS category, year, gdp_growth_pct, inflation_pct
 FROM ghana_macro_indicators
 ORDER BY gdp_growth_pct DESC LIMIT 5)
UNION ALL
(SELECT 'Bottom 5', year, gdp_growth_pct, inflation_pct
 FROM ghana_macro_indicators
 ORDER BY gdp_growth_pct ASC LIMIT 5);


-- ── 8. PRIVATE CREDIT DEPTH TREND ───────────────────────────────────
SELECT
    year,
    private_credit_pct_gdp,
    ROUND(private_credit_pct_gdp - LAG(private_credit_pct_gdp)
          OVER (ORDER BY year), 2) AS yoy_change,
    CASE
        WHEN private_credit_pct_gdp > 20 THEN 'Deep'
        WHEN private_credit_pct_gdp > 15 THEN 'Moderate'
        ELSE 'Shallow'
    END AS credit_depth
FROM ghana_macro_indicators
ORDER BY year;
