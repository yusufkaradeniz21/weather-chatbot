import requests

def get_weather(city_name: str):
    """Canlı hava durumu verisini çeker."""
    try:
        # Şehrin koordinatlarını bul
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url).json()
        
        if not geo_res.get("results"):
            return f"{city_name} şehri bulunamadı."
        
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        
        # Hava durumunu çek
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=True"
        weather_res = requests.get(weather_url).json()
        
        curr = weather_res["current_weather"]
        temp = curr["temperature"]
        wind = curr["windspeed"]
        
        return f"{city_name} için hava durumu: Sıcaklık {temp}°C, Rüzgar Hızı {wind} km/s."
    except Exception as e:
        return f"Hata oluştu: {str(e)}"