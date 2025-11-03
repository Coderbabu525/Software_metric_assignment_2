# Defect Inflow Measurement and Forecasting System

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.0-orange)](https://streamlit.io/)

---

## Overview

This repository provides a **Python-based system to measure and forecast weekly software defect inflow**. It is designed to help **project managers** and software teams:

- Analyze historical defect data.
- Predict defect counts for upcoming weeks.
- Plan resource allocation based on forecasted defect inflow.

The system supports multiple forecasting methods, including **Naive**, **Moving Average (MA)**, **Exponentially Weighted Moving Average (EWMA)**, and **Linear Regression**, allowing flexibility in trend analysis.

---

## Included Files

| File | Description |
|------|-------------|
| `defect_forecast_streamlit.py` | Main Streamlit application for defect measurement and forecasting. |
| `defect_inflow_data.csv` | Sample synthetic weekly defect data. |
| `config.json` | Configuration file for forecasting parameters. |
| `forecast_output.csv` | Generated forecast output (created after running the app). |

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/defect-inflow-forecasting.git
cd defect-inflow-forecasting
