import requests

class WeatherManager:
    def __init__(self, api_key, location):
        self.api_key = api_key
        self.location = location

    def get_weather_notification(self):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.location}&appid={self.api_key}&units=metric"
        
        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather_condition = data['weather'][0]['main']
                temperature = data['main']['temp']
                
                # Basic weather alerts
                if weather_condition in ["Rain", "Thunderstorm"]:
                    return f"🌧️ {weather_condition} expected. Consider delaying watering."
                elif weather_condition == "Clear":
                    return f"☀️ Clear skies. Ideal for plant care."
                elif temperature > 30:
                    return f"🔥 High temperature ({temperature}°C). Water plants early!"
                else:
                    return f"🌿 Weather: {weather_condition}, {temperature}°C."

            return "⚠️ Unable to fetch weather data."

        except requests.exceptions.RequestException:
            return "⚠️ Weather service unavailable."