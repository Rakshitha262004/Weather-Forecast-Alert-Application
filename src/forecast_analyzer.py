# forecast_analyzer.py
# Analyzes forecast data using Pandas

import pandas as pd

def analyze_forecast(forecast_list):
    """
    Convert forecast list to DataFrame and compute daily summaries.
    """
    if not forecast_list:
        return pd.DataFrame()

    df = pd.DataFrame(forecast_list)
    df["temperature"] = pd.to_numeric(df["temperature"])
    df["humidity"] = pd.to_numeric(df["humidity"])
    df["rain"] = pd.to_numeric(df["rain"])

    # Daily summary
    daily = df.groupby("date").agg(
        avg_temp=("temperature", "mean"),
        max_temp=("temperature", "max"),
        min_temp=("temperature", "min"),
        avg_humidity=("humidity", "mean"),
        total_rain=("rain", "sum"),
        max_wind=("wind_speed", "max")
    ).round(2).reset_index()

    return df, daily

def get_weather_summary(daily_df):
    """
    Print a human-readable daily forecast summary.
    """
    print("\n" + "="*60)
    print("       📅 5-DAY FORECAST SUMMARY")
    print("="*60)
    for _, row in daily_df.iterrows():
        print(f"\n📆 {row['date']}")
        print(f"   🌡️  Avg Temp   : {row['avg_temp']:.1f}°C  (Max: {row['max_temp']:.1f}°C, Min: {row['min_temp']:.1f}°C)")
        print(f"   💧 Avg Humidity: {row['avg_humidity']:.1f}%")
        print(f"   🌧️  Total Rain  : {row['total_rain']:.1f} mm")
        print(f"   💨 Max Wind    : {row['max_wind']:.1f} km/h")
    print("="*60)