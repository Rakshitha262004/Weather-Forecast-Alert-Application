# main.py
# Entry point — Live API Mode

from src.api_handler import get_current_weather, get_forecast
from src.data_parser import parse_current_weather, parse_forecast
from src.alert_system import check_alerts, check_forecast_alerts
from src.forecast_analyzer import analyze_forecast, get_weather_summary
from src.visualizer import (plot_temperature_trend, plot_humidity_chart,
                             plot_rain_chart, plot_daily_summary)
from src.report_generator import save_weather_report

print("\n" + "="*60)
print("   🌦️  WEATHER FORECAST & ALERT APPLICATION")
print("="*60)

city = input("\nEnter city name: ").strip()
if not city:
    print("[ERROR] City name cannot be empty.")
    exit()

# Fetch data
print(f"\n[INFO] Fetching weather data for '{city}'...")
raw_current = get_current_weather(city)
raw_forecast = get_forecast(city)

if not raw_current:
    print("[ERROR] Could not fetch current weather. Run simulate.py for demo mode.")
    exit()

# Parse
current = parse_current_weather(raw_current)
forecast_list = parse_forecast(raw_forecast) if raw_forecast else []

# Display
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

upcoming = []
if forecast_list:
    df, daily_df = analyze_forecast(forecast_list)
    get_weather_summary(daily_df)
    upcoming = check_forecast_alerts(forecast_list)
    print("\n" + "="*60)
    print("   📡 UPCOMING ALERTS (Forecast)")
    print("="*60)
    for a in upcoming:
        print(f"  {a}")
    plot_temperature_trend(df, current["city"])
    plot_humidity_chart(df, current["city"])
    plot_rain_chart(df, current["city"])
    plot_daily_summary(daily_df, current["city"])
    save_weather_report(current, df, alerts + upcoming)
    print("\n✅ Done. Charts saved in /outputs, report in /reports.\n")
else:
    print("[WARNING] Forecast not available.")