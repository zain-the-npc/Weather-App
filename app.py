import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os
import random
from api.weather_api import get_weather_data
import streamlit.components.v1 as components
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="Atmosync - Real-time Weather & Air Quality",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Real-time atmospheric intelligence. Sync with your environment."
    }
)

# --- Inject Custom Fonts and CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=Open+Sans:wght@700&family=Roboto+Mono&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Load custom CSS
try:
    with open("utils/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("`styles.css` not found! Please ensure it's in `utils/styles.css` relative to your `app.py`.")


# --- Audio Playback Function (Helper) ---
def play_background_sound(sound_path):
    """Embeds an autoplaying, looping audio file."""
    if not os.path.exists(sound_path):
        return

    try:
        with open(sound_path, "rb") as audio:
            b64 = base64.b64encode(audio.read()).decode("utf-8")
            components.html(f"""
                <audio autoplay loop controls style="display:none;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """, height=0)
    except Exception as e:
        pass


# --- Main Application UI ---

# Custom Hero Header
st.markdown("<h1 class='app-title'>ATMOSYNC</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Sync with your atmosphere.</p>", unsafe_allow_html=True)

# City input with improved styling
city = st.text_input("Enter city name", placeholder="e.g., Wolverhampton, New York, London", key="city_input")

# --- Weather Data Fetching and Display ---
results_placeholder = st.empty()

if city:
    with st.spinner("Fetching weather data..."):
        weather = get_weather_data(city)

    if weather:
        with results_placeholder.container():
            # --- Weather Result Card ---
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)

            # Card Header
            st.markdown(f"<h3 class='weather-card-header'>📍 Weather in {weather['city']}, {weather['country']}</h3>", unsafe_allow_html=True)

            # Main Temperature Display
            st.markdown(f"<p class='main-temp'>{weather['temp']}°C</p>", unsafe_allow_html=True)

            # Weather Parameters
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(f"""
                    <div class='weather-param'>
                        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 8px;'>
                            <span style='font-size: 1.2rem;'>🌤️</span>
                            <span style='font-weight: 600; color: #a0c8ff;'>Condition</span>
                        </div>
                        <div style='font-size: 1.1rem; font-weight: 700;'>{weather['condition']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class='weather-param'>
                        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 8px;'>
                            <span style='font-size: 1.2rem;'>💧</span>
                            <span style='font-weight: 600; color: #a0c8ff;'>Humidity</span>
                        </div>
                        <div style='font-size: 1.1rem; font-weight: 700;'>{weather['humidity']}%</div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div class='weather-param'>
                        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 8px;'>
                            <span style='font-size: 1.2rem;'>🌬️</span>
                            <span style='font-weight: 600; color: #a0c8ff;'>Wind Speed</span>
                        </div>
                        <div style='font-size: 1.1rem; font-weight: 700;'>{weather['wind_kph']} kph</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class='weather-param'>
                        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 8px;'>
                            <span style='font-size: 1.2rem;'>☁️</span>
                            <span style='font-weight: 600; color: #a0c8ff;'>Cloud Cover</span>
                        </div>
                        <div style='font-size: 1.1rem; font-weight: 700;'>{weather.get('cloud', 'N/A')}%</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            
            # --- Air Quality Card ---
            if 'air_quality' in weather:
                st.markdown('<div class="air-quality-card">', unsafe_allow_html=True)
                
                aqi_data = weather['air_quality']
                
                # Determine AQI level
                aqi_index = aqi_data.get('us_epa_index') or aqi_data.get('gb_defra_index')
                aqi_text = "Unknown"
                aqi_color = "#666666"
                
                if aqi_index:
                    aqi_levels = {
                        1: ("Good", "#00E400"),
                        2: ("Moderate", "#FFFF00"),
                        3: ("Unhealthy for Sensitive Groups", "#FF7E00"),
                        4: ("Unhealthy", "#FF0000"),
                        5: ("Very Unhealthy", "#8F3F97"),
                        6: ("Hazardous", "#7E0023")
                    }
                    aqi_text, aqi_color = aqi_levels.get(aqi_index, ("Unknown", "#666666"))
                
                # Air Quality Header
                if aqi_index:
                    st.markdown(f"""
                        <h4 style='margin-bottom: 15px;'>
                            <span class='icon'>🌫️</span> Air Quality: 
                            <span style='color: {aqi_color}; font-weight: 700;'>{aqi_text} (AQI: {aqi_index}/6)</span>
                        </h4>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <h4 style='margin-bottom: 15px;'>
                            <span class='icon'>🌫️</span> Air Quality: 
                            <span style='color: {aqi_color}; font-weight: 700;'>{aqi_text}</span>
                        </h4>
                    """, unsafe_allow_html=True)
                
                # Air Quality Parameters
                aq_col1, aq_col2, aq_col3 = st.columns(3)
                
                with aq_col1:
                    st.markdown(f"""
                        <div class='air-quality-param'>
                            <div style='font-size: 0.95rem; color: #a0c8ff; margin-bottom: 8px;'>PM2.5</div>
                            <div style='font-size: 1.3rem; font-weight: 700;'>{aqi_data.get('pm2_5', 'N/A')}</div>
                            <div style='font-size: 0.85rem; color: #888; margin-top: 5px;'>μg/m³</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='air-quality-param'>
                            <div style='font-size: 0.95rem; color: #a0c8ff; margin-bottom: 8px;'>NO₂</div>
                            <div style='font-size: 1.3rem; font-weight: 700;'>{aqi_data.get('no2', 'N/A')}</div>
                            <div style='font-size: 0.85rem; color: #888; margin-top: 5px;'>μg/m³</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with aq_col2:
                    st.markdown(f"""
                        <div class='air-quality-param'>
                            <div style='font-size: 0.95rem; color: #a0c8ff; margin-bottom: 8px;'>PM10</div>
                            <div style='font-size: 1.3rem; font-weight: 700;'>{aqi_data.get('pm10', 'N/A')}</div>
                            <div style='font-size: 0.85rem; color: #888; margin-top: 5px;'>μg/m³</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='air-quality-param'>
                            <div style='font-size: 0.95rem; color: #a0c8ff; margin-bottom: 8px;'>O₃</div>
                            <div style='font-size: 1.3rem; font-weight: 700;'>{aqi_data.get('o3', 'N/A')}</div>
                            <div style='font-size: 0.85rem; color: #888; margin-top: 5px;'>μg/m³</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with aq_col3:
                    st.markdown(f"""
                        <div class='air-quality-param'>
                            <div style='font-size: 0.95rem; color: #a0c8ff; margin-bottom: 8px;'>CO</div>
                            <div style='font-size: 1.3rem; font-weight: 700;'>{aqi_data.get('co_ug_m3', 'N/A')}</div>
                            <div style='font-size: 0.85rem; color: #888; margin-top: 5px;'>μg/m³</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='air-quality-param'>
                            <div style='font-size: 0.95rem; color: #a0c8ff; margin-bottom: 8px;'>SO₂</div>
                            <div style='font-size: 1.3rem; font-weight: 700;'>{aqi_data.get('so2', 'N/A')}</div>
                            <div style='font-size: 0.85rem; color: #888; margin-top: 5px;'>μg/m³</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # --- CHARTS SECTION ---
                st.markdown('<div class="charts-container">', unsafe_allow_html=True)
                
                # 1. POLLUTANT COMPARISON BAR CHART
                st.markdown('<h4 style="margin: 30px 0 15px 0; color: #ffffff;">📊 Pollutant Analysis</h4>', unsafe_allow_html=True)
                
                pollutants = ['PM2.5', 'PM10', 'CO', 'NO₂', 'O₃', 'SO₂']
                values = []
                for poll in ['pm2_5', 'pm10', 'co_ug_m3', 'no2', 'o3', 'so2']:
                    val = aqi_data.get(poll, 0)
                    try:
                        values.append(float(val) if val != 'N/A' else 0)
                    except:
                        values.append(0)
                
                # Create color scale based on safety levels
                colors = []
                safety_limits = {
                    'PM2.5': [12, 35],
                    'PM10': [20, 50],
                    'CO': [4000, 10000],
                    'NO₂': [25, 100],
                    'O₃': [50, 100],
                    'SO₂': [20, 80]
                }
                
                for poll, val in zip(pollutants, values):
                    limits = safety_limits.get(poll, [0, 0])
                    if val < limits[0]:
                        colors.append('#00E400')
                    elif val < limits[1]:
                        colors.append('#FFFF00')
                    else:
                        colors.append('#FF0000')
                
                if any(values):  # Only show chart if we have data
                    fig_bar = px.bar(
                        x=pollutants,
                        y=values,
                        text=[f"{v:.1f}" if v > 0 else "N/A" for v in values],
                        labels={'x': '', 'y': 'μg/m³'},
                        color=colors,
                        color_discrete_map='identity'
                    )
                    
                    fig_bar.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white', size=12),
                        showlegend=False,
                        margin=dict(l=20, r=20, t=20, b=20),
                        height=350
                    )
                    
                    fig_bar.update_traces(
                        textposition='outside',
                        textfont=dict(color='white', size=12),
                        marker_line_color='rgba(255,255,255,0.3)',
                        marker_line_width=1
                    )
                    
                    st.plotly_chart(fig_bar, use_container_width=True, theme=None)
                else:
                    st.info("Air quality data not available for visualization")
                
                # 2. WEATHER GAUGE CHARTS
                st.markdown('<h4 style="margin: 30px 0 15px 0; color: #ffffff;">📈 Weather Metrics</h4>', unsafe_allow_html=True)
                
                gauge_col1, gauge_col2, gauge_col3 = st.columns(3)
                
                with gauge_col1:
                    # Humidity Gauge
                    try:
                        humidity = float(weather['humidity'])
                        fig_humidity = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=humidity,
                            title={'text': "💧 Humidity", 'font': {'color': 'white', 'size': 16}},
                            number={'font': {'color': 'white', 'size': 28}},
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={
                                'axis': {'range': [0, 100], 'tickcolor': 'white'},
                                'bar': {'color': "#3a7bd5"},
                                'steps': [
                                    {'range': [0, 30], 'color': "rgba(0, 210, 255, 0.2)"},
                                    {'range': [30, 70], 'color': "rgba(0, 210, 255, 0.4)"},
                                    {'range': [70, 100], 'color': "rgba(0, 210, 255, 0.6)"}
                                ],
                                'threshold': {
                                    'line': {'color': "white", 'width': 4},
                                    'thickness': 0.75,
                                    'value': humidity
                                }
                            }
                        ))
                        
                        fig_humidity.update_layout(
                            height=250,
                            margin=dict(l=20, r=20, t=50, b=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            font={'color': "white"}
                        )
                        
                        st.plotly_chart(fig_humidity, use_container_width=True, theme=None)
                    except:
                        st.write("Humidity data unavailable")
                
                with gauge_col2:
                    # Wind Speed Gauge
                    try:
                        wind_speed = float(weather['wind_kph'])
                        fig_wind = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=wind_speed,
                            title={'text': "🌬️ Wind Speed", 'font': {'color': 'white', 'size': 16}},
                            number={'suffix': " kph", 'font': {'color': 'white', 'size': 28}},
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={
                                'axis': {'range': [0, 50], 'tickcolor': 'white'},
                                'bar': {'color': "#00d2ff"},
                                'steps': [
                                    {'range': [0, 15], 'color': "rgba(100, 200, 255, 0.2)"},
                                    {'range': [15, 30], 'color': "rgba(100, 200, 255, 0.4)"},
                                    {'range': [30, 50], 'color': "rgba(100, 200, 255, 0.6)"}
                                ]
                            }
                        ))
                        
                        fig_wind.update_layout(
                            height=250,
                            margin=dict(l=20, r=20, t=50, b=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            font={'color': "white"}
                        )
                        
                        st.plotly_chart(fig_wind, use_container_width=True, theme=None)
                    except:
                        st.write("Wind data unavailable")
                
                with gauge_col3:
                    # Cloud Cover Gauge
                    try:
                        cloud_value = float(weather.get('cloud', 0))
                        fig_cloud = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=cloud_value,
                            title={'text': "☁️ Cloud Cover", 'font': {'color': 'white', 'size': 16}},
                            number={'suffix': " %", 'font': {'color': 'white', 'size': 28}},
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={
                                'axis': {'range': [0, 100], 'tickcolor': 'white'},
                                'bar': {'color': "#a0c8ff"},
                                'steps': [
                                    {'range': [0, 30], 'color': "rgba(160, 200, 255, 0.2)"},
                                    {'range': [30, 70], 'color': "rgba(160, 200, 255, 0.4)"},
                                    {'range': [70, 100], 'color': "rgba(160, 200, 255, 0.6)"}
                                ]
                            }
                        ))
                        
                        fig_cloud.update_layout(
                            height=250,
                            margin=dict(l=20, r=20, t=50, b=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            font={'color': "white"}
                        )
                        
                        st.plotly_chart(fig_cloud, use_container_width=True, theme=None)
                    except:
                        st.write("Cloud data unavailable")
                
                st.markdown('</div>', unsafe_allow_html=True)
                # --- END CHARTS SECTION ---
            
            # --- Dynamic Mood Quote ---
            quotes = {
                'rain': "☔ Cozy weather ideal for staying in with a hot drink.",
                'clear': "🌞 Optimal conditions for productivity and clarity.",
                'cloud': "☁️ Balanced atmosphere for focused work.",
                'wind': "🍃 Dynamic conditions bringing fresh perspectives.",
                'overcast': "☁️ Stable atmospheric pressure for sustained focus.",
                'mist': "🌫️ Reduced visibility suggests inward reflection.",
                'snow': "❄️ Crystalline structures indicate precision opportunities."
            }

            found_quote = False
            for key, quote_text in quotes.items():
                if key in weather['condition'].lower():
                    st.markdown(f'<p class="mood-quote">{quote_text}</p>', unsafe_allow_html=True)
                    found_quote = True
                    break
            
            if not found_quote:
                st.markdown(f'<p class="mood-quote">Unique atmospheric conditions present special opportunities.</p>', unsafe_allow_html=True)

            # --- Background Sound ---
            sound_file = None
            if "rain" in weather['condition'].lower():
                sound_file = "assets/rainy.mp3"
            elif "clear" in weather['condition'].lower():
                sound_file = "assets/sunny.mp3"
            elif "wind" in weather['condition'].lower():
                sound_file = "assets/breezy.mp3"
            elif "cloud" in weather['condition'].lower() or "overcast" in weather['condition'].lower():
                sound_file = "assets/cloudy.mp3"

            if sound_file:
                play_background_sound(sound_file)

    else:
        results_placeholder.error("City not found or error fetching data. Please check the spelling or try another city.")

# --- Advanced Footer ---
st.markdown("""
    <div style="text-align: center; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="color: rgba(255, 255, 255, 0.3); font-size: 0.85rem; letter-spacing: 1px; font-family: 'IBM Plex Sans', sans-serif;">
            ATMOSYNC • ATMOSPHERIC INTELLIGENCE PLATFORM
        </p>
        <p style="color: rgba(255, 255, 255, 0.2); font-size: 0.75rem; margin-top: 5px; font-family: 'IBM Plex Sans', sans-serif;">
            Real-time data synchronization • Predictive environmental analytics
        </p>
    </div>
""", unsafe_allow_html=True)