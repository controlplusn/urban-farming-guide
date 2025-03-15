import requests

class WeatherManager:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def get_weather_notification(self):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&hourly=temperature_2m,precipitation&current_weather=true"

        try:
            response = requests.get(url)
            data = response.json()

            if 'current_weather' in data:
                weather_condition = data['current_weather']['weathercode']
                temperature = data['current_weather']['temperature']

                # Basic weather alerts based on weather codes
                if weather_condition in [61, 63, 65, 80, 81, 82]:  # Rain codes
                    return f"\n🌧️ Rain expected. Consider delaying watering."
                elif weather_condition in [0]:  # Clear sky code
                    return f"\n☀️ Clear skies. Ideal for plant care."
                elif temperature > 30:
                    return f"\n🔥 High temperature ({temperature}°C). Water plants early!"
                else:
                    return f"\n🌿 Weather: Code {weather_condition}, {temperature}°C."

            return "⚠️ Unable to fetch weather data."

        except requests.exceptions.RequestException:
            return "⚠️ Weather service unavailable."
