# romanian-energy-market-analysis
Hydroelectric energy market analysis for Romania (2015-2025):  XGBoost price forecasting, Merit Order modeling,  KMeans clustering and financial performance analysis  of Hidroelectrica S.A. | Python, Pandas, Scikit-Learn, XGBoost

 Romanian Energy Market Analysis

## Overview
Analysis of electricity price drivers and Hidroelectrica S.A. 
financial performance (2015-2025) using machine learning models.

## Key Results
- XGBoost R²=0.909 for electricity price prediction (normal market)
- Merit Order confirmed: EUR/RON dominates with 68% feature importance
- Crisis regime (2022-2023) identified via KMeans clustering

## Data Sources
- ENTSO-E Transparency Platform (generation, load, prices)
- BNR (EUR/RON exchange rate)
- Hidroelectrica S.A. Annual Reports (2015-2024)

## Models
| Model | R² | MAE |
|---|---|---|
| XGBoost (tuned) | 0.844 | 96.5 |
| XGBoost (no crisis) | 0.909 | 32.1 |
| Random Forest | 0.815 | 104.7 |
| OLS Regression | 0.841 | - |
