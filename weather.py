import streamlit as st
import requests
import csv
import os
from datetime import datetime

st.set_page_config(page_title="🌤️ Smart Weather App", layout="centered")
st.title("🌧️ Rain Prediction Dashboard")

city = st.text_input("Enter city name", "Chennai")

if city:
    api_key = "fbbb46c158304622b7382509252606"  # Replace with real key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

	

        # Extract info
        location = data["location"]["name"]
        temp_c = data["current"]["temp_c"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]
        condition = data["current"]["condition"]["text"]
        icon_url = "https:" + data["current"]["condition"]["icon"]

        st.subheader(f"📍 Weather in {location}")
        st.image(icon_url, width=80)
        st.write(f"**Condition:** {condition}")
        st.write(f"🌡️ Temperature: {temp_c} °C")
        st.write(f"💧 Humidity: {humidity}%")
        st.write(f"🌬️ Wind: {wind_kph} kph")

        # Normalize condition text
        condition_lower = condition.lower()

                # Predict rain level
        if any(word in condition_lower for word in ["torrential", "heavy rain"]) or (humidity > 95 and wind_kph > 30):
            rain_level = "🌩️ Heavy rain alert!"
            st.error(rain_level)

        elif any(word in condition_lower for word in ["moderate rain", "patchy rain"]) or (humidity > 85 and wind_kph > 20):
            rain_level = "🌧️ Moderate rain expected."
            st.warning(rain_level)

        elif any(word in condition_lower for word in ["light rain", "showers", "drizzle"]) or (humidity > 70 and wind_kph > 15):
            rain_level = "🌦️ Light rain or drizzle possible."
            st.info(rain_level)

        else:
            rain_level = "☀️ No rain likely."
            st.success(rain_level)

        # ✅ Now rain_level is guaranteed to be defined
        st.caption(f"Reason: Condition = '{condition}', Humidity = {humidity}%, Wind = {wind_kph} kph")

        # 🔄 Save to CSV
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, location, condition, temp_c, humidity, wind_kph, rain_level]

        csv_file = "daily_weather_log.csv"
        file_exists = os.path.exists(csv_file)

        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "City", "Condition", "Temp (°C)", "Humidity (%)", "Wind (kph)", "Rain Status"])
            writer.writerow(row)

        st.success("✅ This record has been saved to daily_weather_log.csv")

