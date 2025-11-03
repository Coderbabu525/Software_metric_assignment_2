import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

st.title("Defect Inflow Measurement and Forecasting System")

# ----------------------------
# Load CSV
# ----------------------------
uploaded_file = st.file_uploader("Upload weekly defect data CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("defect_inflow_data.csv")

# ----------------------------
# Detect defect column automatically
# ----------------------------
possible_cols = [c for c in df.columns if "defect" in c.lower()]
if not possible_cols:
    st.error("❌ Could not find a column with defect counts. Please check your CSV.")
    st.stop()
df.rename(columns={possible_cols[0]: "defects_reported"}, inplace=True)

# Detect week column automatically
possible_weeks = [c for c in df.columns if "week" in c.lower()]
if not possible_weeks:
    st.error("❌ Could not find a column with week start dates. Please check your CSV.")
    st.stop()
df.rename(columns={possible_weeks[0]: "week_start"}, inplace=True)

st.write("### Raw Data", df.head())

# ----------------------------
# Load configuration
# ----------------------------
with open("config.json") as f:
    config = json.load(f)

method = st.selectbox("Forecasting Method", ["naive", "moving_average", "ewma", "linear"], index=1)
window = st.slider("Window Size (for MA/EWMA)", 2, 10, config.get("window_size", 3))
horizon = st.slider("Forecast Weeks Ahead", 1, 6, config.get("forecast_weeks", 4))
alpha = st.slider("EWMA alpha", 0.1, 0.9, config.get("alpha", 0.3))

y = df["defects_reported"].values

# ----------------------------
# Forecast logic
# ----------------------------
forecast = []

if method == "naive":
    forecast = [y[-1]] * horizon

elif method == "moving_average":
    # Compute rolling moving average for each forecast step
    data = list(y)
    for _ in range(horizon):
        ma = np.mean(data[-window:]) if len(data) >= window else np.mean(data)
        forecast.append(ma)
        data.append(ma)  # update for next step

elif method == "ewma":
    # Exponentially weighted moving average
    data = list(y)
    for _ in range(horizon):
        s = data[0]
        for val in data[1:]:
            s = alpha * val + (1 - alpha) * s
        forecast.append(s)
        data.append(s)  # update for next step

elif method == "linear":
    x = np.arange(len(y))
    coef = np.polyfit(x, y, 1)
    forecast = list(np.polyval(coef, np.arange(len(y), len(y)+horizon)))

# ----------------------------
# Prepare forecast dataframe
# ----------------------------
future_weeks = pd.date_range(
    start=pd.to_datetime(df["week_start"]).iloc[-1] + pd.Timedelta(weeks=1),
    periods=horizon,
    freq="W"
)
forecast_df = pd.DataFrame({
    "week_start": future_weeks.strftime("%Y-%m-%d"),
    "forecast_defects": np.round(forecast).astype(int)
})

st.write("### Forecast", forecast_df)

# ----------------------------
# Plot results
# ----------------------------
fig, ax = plt.subplots()
ax.plot(df["week_start"], df["defects_reported"], label="Historical", marker="o")
ax.plot(forecast_df["week_start"], forecast_df["forecast_defects"], label="Forecast", marker="x")
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)

# ----------------------------
# Derived indicators
# ----------------------------
total_defects = df["defects_reported"].sum()
avg_weekly = df["defects_reported"].mean()
max_weekly = df["defects_reported"].max()
st.write("### Indicators")
st.write(f"Total defects (year): {total_defects}")
st.write(f"Average weekly defects: {avg_weekly:.1f}")
st.write(f"Peak weekly defects: {max_weekly}")

# ----------------------------
# Save forecast result
# ----------------------------
forecast_df.to_csv("forecast_output.csv", index=False)
st.success("Forecast results saved as forecast_output.csv")
