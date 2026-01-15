import requests

API_KEY = "4dc756b5fe1e462983972458252807" 

def get_weather_data(city):
    try:
        # CHANGED: Added &aqi=yes to get air quality data
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=yes"
        response = requests.get(url)
        if response.status_code == 200:
            res = response.json()
            
            # Get air quality data if available
            air_quality = res.get("current", {}).get("air_quality")
            
            weather_data = {
                "city": res["location"]["name"],
                "country": res["location"]["country"],
                "temp": res["current"]["temp_c"],
                "condition": res["current"]["condition"]["text"],
                "icon": res["current"]["condition"]["icon"],
                "humidity": res["current"]["humidity"],
                "wind_kph": res["current"]["wind_kph"],
                "cloud": res["current"]["cloud"]
            }
            
            # ADDED: Include air quality data if available
            if air_quality:
                # Convert CO from ppb to µg/m³
                # Conversion factor: 1 ppb CO = 1.145 µg/m³ at 25°C and 1 atm
                co_ppb = air_quality.get("co")
                co_ug_m3 = None
                if co_ppb is not None:
                    co_ug_m3 = round(co_ppb * 1.145, 2)
                
                weather_data["air_quality"] = {
                    "us_epa_index": air_quality.get("us-epa-index"),
                    "gb_defra_index": air_quality.get("gb-defra-index"),
                    "co_ppb": co_ppb,  # Keep original ppb value
                    "co_ug_m3": co_ug_m3,  # Add converted µg/m³ value
                    "no2": air_quality.get("no2"),
                    "o3": air_quality.get("o3"),
                    "so2": air_quality.get("so2"),
                    "pm2_5": air_quality.get("pm2_5"),
                    "pm10": air_quality.get("pm10")
                }
            
            return weather_data
        else:
            return None
    except:
        return None