# streamlit_app.py
# Streamlit Weather Dashboard — Full Theme

import streamlit as st
import json
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Import project modules
from src.data_parser import parse_current_weather, parse_forecast
from src.alert_system import check_alerts, check_forecast_alerts
from src.forecast_analyzer import analyze_forecast
from src.report_generator import save_weather_report

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="WeatherSense | Forecast & Alert",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS Theme ───────────────────────────────────────────
st.markdown("""
<style>
    /* Dark weather theme */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: #e0e0e0;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #56CCF2, #2F80ED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px 0;
        letter-spacing: 2px;
    }
    .subtitle {
        text-align: center;
        color: #aab8c2;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    .weather-card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: 0.3s;
    }
    .weather-card:hover {
        background: rgba(255,255,255,0.12);
        transform: translateY(-2px);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #56CCF2;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #aab8c2;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .alert-box-red {
        background: rgba(231, 76, 60, 0.2);
        border-left: 4px solid #e74c3c;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        color: #ff8a80;
    }
    .alert-box-blue {
        background: rgba(52, 152, 219, 0.2);
        border-left: 4px solid #3498db;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        color: #82cfff;
    }
    .alert-box-green {
        background: rgba(46, 204, 113, 0.2);
        border-left: 4px solid #2ecc71;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        color: #a8f0c6;
    }
    .alert-box-yellow {
        background: rgba(241, 196, 15, 0.18);
        border-left: 4px solid #f1c40f;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        color: #ffe58f;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #56CCF2;
        border-bottom: 2px solid rgba(86,204,242,0.3);
        padding-bottom: 6px;
        margin-bottom: 16px;
    }
    div[data-testid="stSidebar"] {
        background: rgba(15, 32, 39, 0.95) !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #2F80ED, #56CCF2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: 0.3s;
    }
    .stButton > button:hover {
        opacity: 0.88;
        transform: scale(1.02);
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(86,204,242,0.4);
        border-radius: 10px;
        color: white;
        font-size: 1rem;
    }
    .footer {
        text-align: center;
        color: #5d7a8a;
        font-size: 0.8rem;
        margin-top: 30px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Helper: Weather Emoji ───────────────────────────────────────
def weather_emoji(description):
    desc = description.lower()
    if "thunderstorm" in desc: return "⛈️"
    if "rain" in desc or "drizzle" in desc: return "🌧️"
    if "snow" in desc: return "❄️"
    if "cloud" in desc: return "☁️"
    if "clear" in desc: return "☀️"
    if "mist" in desc or "fog" in desc: return "🌫️"
    if "haze" in desc: return "🌁"
    return "🌡️"

def alert_class(alert):
    if "HEAT" in alert or "🔴" in alert: return "alert-box-red"
    if "COLD" in alert or "🔵" in alert: return "alert-box-blue"
    if "STORM" in alert or "WIND" in alert: return "alert-box-yellow"
    if "✅" in alert: return "alert-box-green"
    return "alert-box-yellow"

# ─── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌦️ WeatherSense")
    st.markdown("---")
    mode = st.radio("Data Mode", ["🧪 Simulation (No API)", "🌐 Live API"])
    
    city_input = ""
    if "API" in mode:
        city_input = st.text_input("Enter City Name", placeholder="e.g. Bengaluru")
    
    st.markdown("---")
    st.markdown("### ⚙️ Alert Thresholds")
    high_temp = st.slider("High Temp Alert (°C)", 30, 50, 40)
    low_temp  = st.slider("Low Temp Alert (°C)", -10, 15, 5)
    humidity  = st.slider("Humidity Alert (%)", 60, 100, 85)
    wind      = st.slider("Wind Speed Alert (km/h)", 20, 100, 50)
    
    thresholds = {
        "high_temp": high_temp,
        "low_temp": low_temp,
        "high_humidity": humidity,
        "high_wind": wind,
        "heavy_rain": 10
    }
    
    st.markdown("---")
    run_btn = st.button("🔍 Get Weather")

# ─── Header ─────────────────────────────────────────────────────
st.markdown('<div class="main-title">🌦️ WeatherSense</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Intelligent Weather Forecast & Alert Dashboard</div>', unsafe_allow_html=True)

# ─── Main Logic ─────────────────────────────────────────────────
if run_btn:
    raw_current = None
    raw_forecast = None

    if "Simulation" in mode:
        # Load sample data
        try:
            with open("data/sample_weather.json") as f:
                raw_current = json.load(f)
            with open("data/sample_forecast.json") as f:
                raw_forecast = json.load(f)
            st.info("🧪 Running in Simulation Mode using sample data.")
        except FileNotFoundError:
            st.error("Sample data files not found. Make sure data/sample_weather.json exists.")
            st.stop()
    else:
        if not city_input:
            st.warning("Please enter a city name.")
            st.stop()
        try:
            from src.api_handler import get_current_weather, get_forecast
            with st.spinner(f"Fetching weather for {city_input}..."):
                raw_current = get_current_weather(city_input)
                raw_forecast = get_forecast(city_input)
            if not raw_current:
                st.error("City not found or API error. Check your API key in .env file.")
                st.stop()
        except Exception as e:
            st.error(f"API Error: {e}")
            st.stop()

    # Parse
    current = parse_current_weather(raw_current)
    forecast_list = parse_forecast(raw_forecast)
    df, daily_df = analyze_forecast(forecast_list)

    alerts = check_alerts(current, thresholds)
    upcoming = check_forecast_alerts(forecast_list, thresholds)

    city_name = current["city"]
    emoji = weather_emoji(current["description"])

    # ─── Current Weather Banner ──────────────────────────────────
    st.markdown(f"<div class='section-header'>📍 Current Weather — {city_name}, {current['country']}</div>",
                unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    metrics = [
        (f"{emoji}", f"{current['temperature']:.1f}°C", "Temperature"),
        ("🤔", f"{current['feels_like']:.1f}°C", "Feels Like"),
        ("💧", f"{current['humidity']}%", "Humidity"),
        ("💨", f"{current['wind_speed']:.1f} km/h", "Wind Speed"),
        ("👁️", f"{current['visibility']:.1f} km", "Visibility"),
    ]
    for col, (icon, val, label) in zip([col1,col2,col3,col4,col5], metrics):
        with col:
            st.markdown(f"""
            <div class="weather-card">
                <div style="font-size:2rem">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # Condition badge
    st.markdown(f"""
    <div style='text-align:center; margin:14px 0; font-size:1.1rem; color:#56CCF2;'>
        ☁️ Condition: <b>{current['description']}</b> &nbsp;|&nbsp;
        📊 Pressure: <b>{current['pressure']} hPa</b> &nbsp;|&nbsp;
        🌡️ Range: <b>{current['temp_min']:.1f}°C – {current['temp_max']:.1f}°C</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ─── Alerts ──────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-header'>🚨 Current Alerts</div>", unsafe_allow_html=True)
        for alert in alerts:
            css = alert_class(alert)
            st.markdown(f'<div class="{css}">{alert}</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='section-header'>📡 Forecast Alerts</div>", unsafe_allow_html=True)
        for alert in upcoming:
            css = alert_class(alert)
            st.markdown(f'<div class="{css}">{alert}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ─── Forecast Charts ─────────────────────────────────────────
    st.markdown("<div class='section-header'>📈 Forecast Charts</div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Temperature", "💧 Humidity", "🌧️ Rainfall", "📊 Daily Summary"])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["datetime"], y=df["temperature"],
            mode="lines+markers",
            line=dict(color="#FF6B35", width=2.5),
            marker=dict(size=5),
            fill="tozeroy", fillcolor="rgba(255,107,53,0.12)",
            name="Temperature (°C)"
        ))
        fig.add_hline(y=thresholds["high_temp"], line_dash="dash",
                      line_color="red", annotation_text=f"Heat Alert ({thresholds['high_temp']}°C)")
        fig.add_hline(y=thresholds["low_temp"], line_dash="dash",
                      line_color="#56CCF2", annotation_text=f"Cold Alert ({thresholds['low_temp']}°C)")
        fig.update_layout(
            title=f"Temperature Forecast — {city_name}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.04)",
            font=dict(color="#e0e0e0"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)", title="°C"),
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig2 = go.Figure()
        colors = ["#e74c3c" if h >= thresholds["high_humidity"] else "#4A90D9"
                  for h in df["humidity"]]
        fig2.add_trace(go.Bar(
            x=df["datetime"], y=df["humidity"],
            marker_color=colors, name="Humidity (%)"
        ))
        fig2.add_hline(y=thresholds["high_humidity"], line_dash="dash",
                       line_color="red", annotation_text=f"Alert ({thresholds['high_humidity']}%)")
        fig2.update_layout(
            title=f"Humidity Forecast — {city_name}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.04)",
            font=dict(color="#e0e0e0"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)", range=[0,110], title="%"),
            height=380
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        rain_colors = ["#1B4F72" if r < 10 else "#e74c3c" for r in df["rain"]]
        fig3 = go.Figure(go.Bar(
            x=df["datetime"], y=df["rain"],
            marker_color=rain_colors, name="Rainfall (mm)"
        ))
        fig3.add_hline(y=10, line_dash="dash", line_color="red",
                       annotation_text="Heavy Rain (10mm)")
        fig3.update_layout(
            title=f"Rainfall Forecast — {city_name}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.04)",
            font=dict(color="#e0e0e0"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)", title="mm"),
            height=380
        )
        st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=daily_df["date"], y=daily_df["max_temp"],
            name="Max Temp", line=dict(color="#e74c3c", width=2),
            mode="lines+markers"
        ))
        fig4.add_trace(go.Scatter(
            x=daily_df["date"], y=daily_df["min_temp"],
            name="Min Temp", line=dict(color="#56CCF2", width=2),
            fill="tonexty", fillcolor="rgba(86,204,242,0.08)",
            mode="lines+markers"
        ))
        fig4.update_layout(
            title=f"Daily Temperature Range — {city_name}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.04)",
            font=dict(color="#e0e0e0"),
            legend=dict(bgcolor="rgba(0,0,0,0.3)"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)", title="°C"),
            height=380
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # ─── Forecast Table ──────────────────────────────────────────
    st.markdown("<div class='section-header'>📅 Daily Forecast Summary</div>", unsafe_allow_html=True)
    styled = daily_df.rename(columns={
        "date":"Date", "avg_temp":"Avg Temp (°C)",
        "max_temp":"Max Temp (°C)", "min_temp":"Min Temp (°C)",
        "avg_humidity":"Humidity (%)", "total_rain":"Rain (mm)",
        "max_wind":"Max Wind (km/h)"
    })
    st.dataframe(
        styled.style.background_gradient(cmap="RdYlBu_r", subset=["Avg Temp (°C)"]),
        use_container_width=True, hide_index=True
    )

    # ─── Report Download ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("<div class='section-header'>📥 Download Report</div>", unsafe_allow_html=True)

    report_df = df[["datetime","temperature","humidity","wind_speed","description","rain"]].copy()
    csv = report_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Forecast CSV",
        data=csv,
        file_name=f"weather_{city_name}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    # ─── Footer ──────────────────────────────────────────────────
    st.markdown(
        f'<div class="footer">WeatherSense • Built with Python & Streamlit • '
        f'Data from OpenWeatherMap • {datetime.now().strftime("%B %d, %Y")}</div>',
        unsafe_allow_html=True
    )

else:
    # Landing screen
    st.markdown("""
    <div style='text-align:center; padding:60px 20px;'>
        <div style='font-size:5rem;'>🌦️</div>
        <div style='font-size:1.5rem; color:#56CCF2; font-weight:600; margin:16px 0;'>
            Intelligent Weather Monitoring & Alert System
        </div>
        <div style='color:#aab8c2; font-size:1rem; max-width:600px; margin:0 auto;'>
            Select a data mode in the sidebar, configure your alert thresholds,
            and click <b>Get Weather</b> to see live or simulated weather forecasts,
            smart alerts, and interactive charts.
        </div>
        <div style='margin-top:30px; display:flex; justify-content:center; gap:20px; flex-wrap:wrap;'>
            <span style='background:rgba(86,204,242,0.15); border:1px solid #56CCF2;
                         border-radius:20px; padding:6px 16px; color:#56CCF2;'>
                🌡️ Temperature Tracking</span>
            <span style='background:rgba(86,204,242,0.15); border:1px solid #56CCF2;
                         border-radius:20px; padding:6px 16px; color:#56CCF2;'>
                💧 Humidity Monitoring</span>
            <span style='background:rgba(86,204,242,0.15); border:1px solid #56CCF2;
                         border-radius:20px; padding:6px 16px; color:#56CCF2;'>
                🚨 Smart Alerts</span>
            <span style='background:rgba(86,204,242,0.15); border:1px solid #56CCF2;
                         border-radius:20px; padding:6px 16px; color:#56CCF2;'>
                📊 5-Day Forecast</span>
        </div>
    </div>
    """, unsafe_allow_html=True)