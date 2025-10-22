# machine_learning/views.py

import os
import csv
from datetime import datetime, timedelta
import io
import base64
from django.shortcuts import render
from django.conf import settings

# Path to folder holding CSV files (project root / "Raw Data")
RAW_DATA_DIR = os.path.join(settings.BASE_DIR, "Raw Data")


def load_date_price_csv(filename):
    """
    Read CSV (Date, Price) into two lists: dates (datetime.date) and prices (floats).
    """
    path = os.path.join(RAW_DATA_DIR, filename)
    dates = []
    prices = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header row
        for row in reader:
            if not row or len(row) < 2:
                continue
            date_str = row[0].strip()
            price_str = row[1].strip()
            if date_str == "" or price_str == "":
                continue
            # parse date YYYY-MM-DD (adjust if your CSV uses a different format)
            dt = datetime.strptime(date_str, "%d/%m/%Y").date()
            price = float(price_str)
            dates.append(dt)
            prices.append(price)
    return dates, prices

import numpy as np
from scipy import stats
import matplotlib
# Use Agg backend for headless servers
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def create_plot_data_url(dates, prices):
    """
    Fit a simple linear regression on price vs days since first date,
    project 5 years into future (weekly steps), draw a Matplotlib figure,
    return a data URL (data:image/png;base64,...).
    """
    # Sort and convert to numpy arrays
    pairs = sorted(zip(dates, prices), key=lambda x: x[0])
    dates_sorted, prices_sorted = zip(*pairs)
    prices_arr = np.array(prices_sorted, dtype=float)
    first_date = dates_sorted[0]
    time_days = np.array([(d - first_date).days for d in dates_sorted], dtype=float)

    # Train/test split: last 50 weeks as holdout
    holdout_n = 50
    n_total = len(time_days)
    if n_total <= holdout_n:
        holdout_n = max(1, n_total // 2)
    train_end = n_total - holdout_n
    t_train = time_days[:train_end]
    y_train = prices_arr[:train_end]
    t_hold = time_days[train_end:]
    y_hold = prices_arr[train_end:]
    last_date = dates_sorted[-1]
    last_time = time_days[-1]

    # Fit simple linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(t_train, y_train)

    # Project forward 5 years (weekly steps)
    years_future = 5
    weeks_per_year = 52
    future_weeks = years_future * weeks_per_year
    future_dates = []
    future_times = []
    for i in range(1, future_weeks + 1):
        new_date = last_date + timedelta(weeks=i)
        future_dates.append(new_date)
        future_times.append((new_date - first_date).days)
    future_times = np.array(future_times, dtype=float)

    # Predictions
    y_train_pred = intercept + slope * t_train
    y_hold_pred = intercept + slope * t_hold
    y_future_pred = intercept + slope * future_times

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 5))
    # Plot actual points
    ax.plot(dates_sorted[:train_end], y_train, "o", color="blue", label="Train (actual)")
    ax.plot(dates_sorted[train_end:], y_hold, "o", color="orange", label="Holdout (actual)")
    # Fitted historic line
    hist_time_dense = np.linspace(time_days[0], last_time, 200)
    hist_price_fitted = intercept + slope * hist_time_dense
    hist_dates_dense = [first_date + timedelta(days=int(d)) for d in hist_time_dense]
    ax.plot(hist_dates_dense, hist_price_fitted, "--", color="green", label="Fitted (historic)")
    # Future projection
    ax.plot(future_dates, y_future_pred, "-", color="red", label=f"Projection ({years_future} yrs)")
    # Demarcation between history and future
    ax.axvline(x=last_date + timedelta(days=0.5), color="gray", linestyle=":", linewidth=1)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title("Linear regression projection (5-year extension)")
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate()

    # Save to in-memory buffer and encode as base64 data URL
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("ascii")
    return f"data:image/png;base64,{img_b64}"

def eth_plot_view(request):
    """
    Django view: load CSV from Raw Data folder, create plot, render template with embedded image.
    """
    # Filename to use (you can change this later via UI)
    filename = "Price of Ethereum in USD 2017 to 2025.csv"

    # Load CSV and produce data URL for plot
    dates, prices = load_date_price_csv(filename)
    plot_data_url = create_plot_data_url(dates, prices)

    # Render template and pass plot_data_url
    return render(request, "eth_plot.html", {"plot_data_url": plot_data_url, "filename": filename})


## extending views.py to allow user input 



def list_csv_files():
    """Return CSV filenames in RAW_DATA_DIR (simple filter)."""
    try:
        items = os.listdir(RAW_DATA_DIR)
    except Exception:
        return []
    return [f for f in items if f.lower().endswith(".csv")]

def safe_int(val, default):
    try:
        return int(val)
    except Exception:
        return default

def safe_float(val, default):
    try:
        return float(val)
    except Exception:
        return default

def create_plot_data_url_with_params(dates, prices, holdout_n=50, slope_mode="none", slope_value=1.0, years_future=5):
    """Same logic as before but accepts the parameters and applies slope adjustments."""
    pairs = sorted(zip(dates, prices), key=lambda x: x[0])
    dates_sorted, prices_sorted = zip(*pairs)
    prices_arr = np.array(prices_sorted, dtype=float)
    first_date = dates_sorted[0]
    time_days = np.array([(d - first_date).days for d in dates_sorted], dtype=float)

    # Adjust holdout_n defensively
    n_total = len(time_days)
    if n_total <= holdout_n:
        holdout_n = max(1, n_total // 2)
    train_end = n_total - holdout_n

    t_train = time_days[:train_end]
    y_train = prices_arr[:train_end]
    t_hold = time_days[train_end:]
    y_hold = prices_arr[train_end:]
    last_date = dates_sorted[-1]
    last_time = time_days[-1]

    # Fit OLS slope/intercept on training
    slope_fitted, intercept, r_value, p_value, std_err = stats.linregress(t_train, y_train)

    # Apply slope mode:
    if slope_mode == "none":
        slope_used = slope_fitted
    elif slope_mode == "mult":
        slope_used = slope_fitted * slope_value
    else:  # override
        slope_used = slope_value

    # Project forward
    weeks_per_year = 52
    future_weeks = int(years_future) * weeks_per_year
    future_dates = []
    future_times = []
    for i in range(1, future_weeks + 1):
        new_date = last_date + timedelta(weeks=i)
        future_dates.append(new_date)
        future_times.append((new_date - first_date).days)
    future_times = np.array(future_times, dtype=float)

    # Predictions
    y_train_pred = intercept + slope_used * t_train
    y_hold_pred = intercept + slope_used * t_hold
    y_future_pred = intercept + slope_used * future_times

    # Create plot (concise, same as before)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates_sorted[:train_end], y_train, "o", color="blue", label="Train (actual)")
    ax.plot(dates_sorted[train_end:], y_hold, "o", color="orange", label="Holdout (actual)")
    hist_time_dense = np.linspace(time_days[0], last_time, 200)
    hist_price_fitted = intercept + slope_used * hist_time_dense
    hist_dates_dense = [first_date + timedelta(days=int(d)) for d in hist_time_dense]
    ax.plot(hist_dates_dense, hist_price_fitted, "--", color="green", label="Fitted (historic)")
    ax.plot(future_dates, y_future_pred, "-", color="red", label=f"Projection ({years_future} yrs)")
    ax.axvline(x=last_date + timedelta(days=0.5), color="gray", linestyle=":", linewidth=1)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title("Linear regression projection")
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate()

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("ascii")
    return f"data:image/png;base64,{img_b64}", slope_fitted, slope_used, intercept, r_value**2

def eth_plot_view2(request):
    # Available files and defaults
    files = list_csv_files()
    filename = files[0] if files else ""
    holdout_n = 50
    slope_mode = "none"
    slope_value = "1.0"
    years_future = 5

    # If POST, read form values
    if request.method == "POST":
        filename = request.POST.get("filename", filename)
        holdout_n = safe_int(request.POST.get("holdout_n"), holdout_n)
        slope_mode = request.POST.get("slope_mode", slope_mode)
        slope_value = request.POST.get("slope_value", slope_value)
        years_future = safe_int(request.POST.get("years_future"), years_future)

    # Ensure filename exists in folder (prevent path traversal)
    if filename not in files:
        # fallback to first available
        filename = files[0] if files else ""

    # Load CSV (if available)
    dates, prices = [], []
    if filename:
        path = os.path.join(RAW_DATA_DIR, filename)
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                _ = next(reader)
                for row in reader:
                    if not row or len(row) < 2:
                        continue
                    dt = datetime.strptime(row[0].strip(), "%d/%m/%Y").date()
                    prices.append(float(row[1].strip()))
                    dates.append(dt)
        except Exception as e:
            # In production, log the error. For now, show no plot.
            dates, prices = [], []

    plot_data_url = None
    slope_fitted = slope_used = intercept = r2 = None
    if dates and prices:
        # Interpret slope_value as float (for multiplier/override)
        slope_val_float = safe_float(slope_value, 1.0)
        plot_data_url, slope_fitted, slope_used, intercept, r2 = create_plot_data_url_with_params(
            dates, prices, holdout_n=holdout_n, slope_mode=slope_mode, slope_value=slope_val_float, years_future=years_future
        )

    # Render template with context for form defaults and diagnostics
    return render(request, "eth_plot2.html", {
        "files": files,
        "filename": filename,
        "holdout_n": holdout_n,
        "slope_mode": slope_mode,
        "slope_value": slope_value,
        "years_future": years_future,
        "plot_data_url": plot_data_url,
        "slope_fitted": slope_fitted,
        "slope_used": slope_used,
        "intercept": intercept,
        "r2": r2,
    })