# alert_system.py
# Checks weather conditions and generates alerts

# Default thresholds (can be customized)
THRESHOLDS = {
    "high_temp": 40,       # Celsius
    "low_temp": 5,         # Celsius
    "high_humidity": 85,   # Percentage
    "high_wind": 50,       # km/h
    "heavy_rain": 10       # mm in 3 hours
}

def check_alerts(weather_data, thresholds=None):
    """
    Check current weather against alert thresholds.
    Returns list of alert strings.
    """
    if thresholds is None:
        thresholds = THRESHOLDS

    alerts = []
    temp = weather_data.get("temperature", 0)
    humidity = weather_data.get("humidity", 0)
    wind = weather_data.get("wind_speed", 0)
    description = weather_data.get("description", "").lower()

    # Temperature alerts
    if temp >= thresholds["high_temp"]:
        alerts.append(f"🔴 HEAT ALERT: Temperature is {temp:.1f}°C (Threshold: {thresholds['high_temp']}°C)")
    if temp <= thresholds["low_temp"]:
        alerts.append(f"🔵 COLD ALERT: Temperature is {temp:.1f}°C (Threshold: {thresholds['low_temp']}°C)")

    # Humidity alert
    if humidity >= thresholds["high_humidity"]:
        alerts.append(f"💧 HUMIDITY ALERT: Humidity is {humidity}% (Threshold: {thresholds['high_humidity']}%)")

    # Wind alert
    if wind >= thresholds["high_wind"]:
        alerts.append(f"💨 STORM ALERT: Wind speed is {wind:.1f} km/h (Threshold: {thresholds['high_wind']} km/h)")

    # Rain/Storm from description
    rain_keywords = ["rain", "drizzle", "thunderstorm", "snow", "storm"]
    for keyword in rain_keywords:
        if keyword in description:
            alerts.append(f"🌧️ WEATHER ALERT: {weather_data.get('description')} detected!")
            break

    if not alerts:
        alerts.append("✅ All Clear: Weather conditions are normal.")

    return alerts

def check_forecast_alerts(forecast_list, thresholds=None):
    """
    Scan forecast data for upcoming alert conditions.
    Returns list of upcoming alert strings.
    """
    if thresholds is None:
        thresholds = THRESHOLDS

    upcoming_alerts = []
    for entry in forecast_list:
        if entry["temperature"] >= thresholds["high_temp"]:
            upcoming_alerts.append(
                f"⚠️ High temp expected on {entry['datetime']}: {entry['temperature']:.1f}°C"
            )
        if entry["rain"] >= thresholds["heavy_rain"]:
            upcoming_alerts.append(
                f"⚠️ Heavy rain expected on {entry['datetime']}: {entry['rain']} mm"
            )
        if entry["wind_speed"] >= thresholds["high_wind"]:
            upcoming_alerts.append(
                f"⚠️ High wind expected on {entry['datetime']}: {entry['wind_speed']:.1f} km/h"
            )

    return upcoming_alerts if upcoming_alerts else ["✅ No severe weather in forecast."]