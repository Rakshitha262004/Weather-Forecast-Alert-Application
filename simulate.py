# simulate.py
# Run the project without an API key using sample data

import json
from src.data_parser import parse_current_weather, parse_forecast
from src.alert_system import check_alerts, check_forecast_alerts
from src.forecast_analyzer import analyze_forecast, get_weather_summary
from src.visualizer import (plot_temperature_trend, plot_humidity_chart,
                             plot_rain_chart, plot_daily_summary)
from src.report_generator import save_weather_report

print("\n" + "="*60)
print("   🌦️  WEATHER FORECAST & ALERT — SIMULATION MODE")
print("="*60)

# Load sample data
with open("data/sample_weather.json") as f:
    raw_current = json.load(f)

with open("data/sample_forecast.json") as f:
    raw_forecast = json.load(f)

# Parse data
current = parse_current_weather(raw_current)
forecast_list = parse_forecast(raw_forecast)

# Display current weather
print(f"\n📍 City       : {current['city']}, {current['country']}")
print(f"🌡️  Temperature : {current['temperature']:.1f}°C (Feels like {current['feels_like']:.1f}°C)")
print(f"💧 Humidity   : {current['humidity']}%")
print(f"💨 Wind Speed : {current['wind_speed']:.1f} km/h")
print(f"☁️  Condition  : {current['description']}")
print(f"👁️  Visibility : {current['visibility']:.1f} km")

# Alerts
print("\n" + "="*60)
print("   🚨 CURRENT WEATHER ALERTS")
print("="*60)
alerts = check_alerts(current)
for alert in alerts:
    print(f"  {alert}")

# Forecast analysis
df, daily_df = analyze_forecast(forecast_list)
get_weather_summary(daily_df)

# Forecast alerts
print("\n" + "="*60)
print("   📡 UPCOMING ALERTS (Forecast)")
print("="*60)
upcoming = check_forecast_alerts(forecast_list)
for a in upcoming:
    print(f"  {a}")

# Charts
print("\n[INFO] Generating charts...")
plot_temperature_trend(df, current["city"])
plot_humidity_chart(df, current["city"])
plot_rain_chart(df, current["city"])
plot_daily_summary(daily_df, current["city"])

# Report
save_weather_report(current, df, alerts + upcoming)

print("\n✅ Simulation complete. Check /outputs and /reports folders.\n")