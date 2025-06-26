import streamlit as st
import requests

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

        # Smart rain logic
        if any(word in condition_lower for word in ["torrential", "heavy rain"]) or (humidity > 95 and wind_kph > 30):
            st.error("🌩️ Heavy rain alert!")
            st.caption(f"Because: Condition is '{condition}', Humidity is {humidity}%, Wind is {wind_kph} kph")

        elif any(word in condition_lower for word in ["moderate rain", "patchy rain"]) or (humidity > 85 and wind_kph > 20):
            st.warning("🌧️ Moderate rain expected.")
            st.caption(f"Because: Condition is '{condition}', Humidity is {humidity}%, Wind is {wind_kph} kph")

        elif any(word in condition_lower for word in ["light rain", "showers", "drizzle"]) or (humidity > 70 and wind_kph > 15):
            st.info("🌦️ Light rain or drizzle possible.")
            st.caption(f"Because: Condition is '{condition}', Humidity is {humidity}%, Wind is {wind_kph} kph")

        else:
            st.success("☀️ No rain likely.")
            st.caption(f"Because: Condition is '{condition}', Humidity is {humidity}%, Wind is {wind_kph} kph")

    else:
        st.error("❌ Could not fetch data. Check city name or try again.")
