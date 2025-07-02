from handlers.weather_handler import get_weather_summary

print(get_weather_summary("Charlotte", mode="current"))
print(get_weather_summary("Matthews", mode="hourly"))
print(get_weather_summary("Matthews", mode="daily"))
