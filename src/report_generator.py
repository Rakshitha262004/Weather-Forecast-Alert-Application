# report_generator.py

import pandas as pd
import os
from datetime import datetime

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def save_weather_report(current_weather, forecast_df, alerts):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    city = current_weather.get("city", "unknown")

    filename = f"weather_report_{city}_{timestamp}.csv"
    filepath = os.path.join(REPORT_DIR, filename)

    # Current weather row
    current_row = {
        "type": "Current",
        "datetime": current_weather.get("timestamp"),
        "temperature": current_weather.get("temperature"),
        "humidity": current_weather.get("humidity"),
        "wind_speed": current_weather.get("wind_speed"),
        "description": current_weather.get("description"),
        "rain": 0
    }

    # Forecast rows
    forecast_rows = forecast_df[
        ["datetime", "temperature", "humidity",
         "wind_speed", "description", "rain"]
    ].copy()

    forecast_rows["type"] = "Forecast"

    # Combine
    report_df = pd.concat(
        [pd.DataFrame([current_row]), forecast_rows],
        ignore_index=True
    )

    report_df.to_csv(filepath, index=False)

    print(f"[INFO] Report saved: {filepath}")

    # Save alerts
    alert_file = os.path.join(
        REPORT_DIR,
        f"alerts_{city}_{timestamp}.txt"
    )

    with open(alert_file, "w", encoding="utf-8") as f:

        f.write(f"Weather Alerts — {city}\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write("=" * 50 + "\n")

        for alert in alerts:
            f.write(alert + "\n")

    print(f"[INFO] Alerts saved: {alert_file}")

    return filepath