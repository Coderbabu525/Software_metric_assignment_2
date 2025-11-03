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
```

2. Install required Python packages (recommended to use a virtual environment):

```bash
  pip install streamlit pandas numpy matplotlib
```

## Usage
- Run the Streamlit app:
  ```bash
  streamlit run defect_forecast_streamlit.py
  ```
- Upload defect data CSV (optional). If not uploaded, the app uses the provided synthetic data (defect_inflow_data.csv).
- View raw data: The first few rows of historical weekly defects are displayed.
- Select forecast method: Choose between Naive, Moving Average, EWMA, or Linear.
- Adjust parameters:
    Window Size for MA/EWMA
    Forecast Weeks Ahead (1–6 weeks)
    EWMA alpha (if using EWMA)
- View forecast: Displays a table of predicted defects for the selected horizon.
- Visualize: Historical vs forecasted defects are plotted.
- Derived indicators: Total defects, average weekly defects, and peak weekly defects are displayed.
- Export results: Forecasted defects are saved as forecast_output.csv.


## Data
- Synthetic Data: defect_inflow_data.csv simulates weekly defect inflow with seasonality patterns.
- Columns:
    week_start: Start date of the week (YYYY-MM-DD)
    defects_reported: Number of defects reported during that week
You can replace the synthetic CSV with your own project defect data. The app dynamically adjusts based on the uploaded CSV.


## Metrics Explained
- Total Defects: Sum of all defects reported in the historical period.
- Average Weekly Defects: Mean defects per week.
- Peak Weekly Defects: Maximum defects observed in a week.
- Forecasted Defects: Predicted number of defects for upcoming weeks using the selected model.



# Code Churn Measurement Instrument

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
[![Git](https://img.shields.io/badge/git-required-green)](https://git-scm.com/)

---

## Overview

This repository provides a **Python-based instrument to measure Code Churn** in a Git repository.  

**Code Churn** is a software metric that quantifies the amount of code change over time. It helps stakeholders, such as project managers and developers, to:

- Understand development activity.
- Identify high-change areas of the code.
- Assess risk in frequently modified files.
- Support resource allocation decisions.

This instrument analyzes **lines added**, **lines removed**, and **total churn** per file and per module in a Git repository.

---

## Definitions

- **Code Churn**: The sum of lines added and lines removed in a source code file or module over time.  
- **Lines Added**: Number of new lines of code introduced.  
- **Lines Removed**: Number of lines deleted or modified.  
- **Total Churn**: `Lines Added + Lines Removed` for a file or module.  
- **Module**: Any folder in the repository containing source code files; aggregation is done per module.  

---


## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/code-churn-instrument.git
cd code-churn-instrument
```
2. Install Python dependencies:
```bash
pip install matplotlib
```
3. Ensure you have Git installed and a local clone of the repository


## Usage
Run the measurement instrument on a Git repository
```bash
python3 code_churn_measurement.py --repo /path/to/git/repo --out churn_results.json
```
- --repo-> path to the local git repository
- --out-> path to save the JSON results




