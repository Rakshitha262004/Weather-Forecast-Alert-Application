# visualizer.py
# Creates weather charts using Matplotlib

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for saving files
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
from datetime import datetime

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_temperature_trend(df, city):
    """
    Line chart of temperature over forecast period.
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["datetime"], df["temperature"],
            color="#FF6B35", marker="o", linewidth=2, markersize=4, label="Temperature (°C)")
    ax.fill_between(df["datetime"], df["temperature"], alpha=0.15, color="#FF6B35")
    ax.set_title(f"Temperature Forecast — {city}", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Date & Time", fontsize=11)
    ax.set_ylabel("Temperature (°C)", fontsize=11)
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "temperature_chart.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[INFO] Temperature chart saved: {path}")
    return path

def plot_humidity_chart(df, city):
    """
    Bar chart of humidity across forecast period.
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(df["datetime"], df["humidity"],
                  color="#4A90D9", alpha=0.8, width=0.08)
    ax.axhline(y=85, color="red", linestyle="--", linewidth=1.5, label="Alert Threshold (85%)")
    ax.set_title(f"Humidity Forecast — {city}", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Date & Time", fontsize=11)
    ax.set_ylabel("Humidity (%)", fontsize=11)
    ax.set_ylim(0, 110)
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, linestyle="--", alpha=0.4, axis="y")
    ax.legend()
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "humidity_chart.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[INFO] Humidity chart saved: {path}")
    return path

def plot_rain_chart(df, city):
    """
    Bar chart of rain amounts across forecast period.
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(df["datetime"], df["rain"],
           color="#1B4F72", alpha=0.8, width=0.08, label="Rain (mm)")
    ax.set_title(f"Rainfall Forecast — {city}", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Date & Time", fontsize=11)
    ax.set_ylabel("Rainfall (mm)", fontsize=11)
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, linestyle="--", alpha=0.4, axis="y")
    ax.legend()
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "rain_chart.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[INFO] Rain chart saved: {path}")
    return path

def plot_daily_summary(daily_df, city):
    """
    Multi-panel daily summary chart.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(f"Daily Weather Summary — {city}", fontsize=16, fontweight="bold")

    # Max/Min temperature
    ax1 = axes[0, 0]
    ax1.plot(daily_df["date"], daily_df["max_temp"], "r-o", label="Max Temp")
    ax1.plot(daily_df["date"], daily_df["min_temp"], "b-o", label="Min Temp")
    ax1.fill_between(daily_df["date"], daily_df["min_temp"], daily_df["max_temp"], alpha=0.1, color="orange")
    ax1.set_title("Temperature Range (°C)")
    ax1.legend()
    ax1.tick_params(axis="x", rotation=30)
    ax1.grid(True, alpha=0.3)

    # Average humidity
    ax2 = axes[0, 1]
    ax2.bar(daily_df["date"], daily_df["avg_humidity"], color="#4A90D9", alpha=0.8)
    ax2.axhline(85, color="red", linestyle="--", label="Alert Level")
    ax2.set_title("Average Humidity (%)")
    ax2.legend()
    ax2.tick_params(axis="x", rotation=30)
    ax2.grid(True, alpha=0.3, axis="y")

    # Total rainfall
    ax3 = axes[1, 0]
    ax3.bar(daily_df["date"], daily_df["total_rain"], color="#1B4F72", alpha=0.8)
    ax3.set_title("Total Rainfall (mm)")
    ax3.tick_params(axis="x", rotation=30)
    ax3.grid(True, alpha=0.3, axis="y")

    # Max wind speed
    ax4 = axes[1, 1]
    ax4.plot(daily_df["date"], daily_df["max_wind"], "g-o", linewidth=2)
    ax4.axhline(50, color="red", linestyle="--", label="Storm Threshold")
    ax4.set_title("Max Wind Speed (km/h)")
    ax4.legend()
    ax4.tick_params(axis="x", rotation=30)
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "daily_summary_chart.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[INFO] Daily summary chart saved: {path}")
    return path