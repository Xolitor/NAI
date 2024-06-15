from http import client
import os
import requests
from collections import defaultdict
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

news_api_id = os.environ.get("NEWS_API_KEY")
weather_api_id = os.environ.get("WEATHER_API_KEY")

def get_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])[:10]
            final_news = []
            for article in articles:
                title = article["title"]
                description = article["description"]
                source_name = article["source"]["name"]
                url = article["url"]
                author = article["author"]
                title_description = f"""
                **Title**: {title}
                **Author**: {author}
                **Source**: {source_name}
                **Description**: {description}
                [Read more]({url})
                """
                final_news.append(title_description)
            return final_news
    except requests.exceptions.RequestException as e:
        st.error("Error occurred during API request")
        return []

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api_id}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            city_name = data["city"]["name"]
            country = data["city"]["country"]
            daily_forecasts = defaultdict(list)
            
            for forecast in data["list"]:
                date = forecast["dt_txt"].split(" ")[0]
                temperature = forecast["main"]["temp"]
                feels_like = forecast["main"]["feels_like"]
                description = forecast["weather"][0]["description"]
                wind_speed = forecast["wind"]["speed"]
                humidity = forecast["main"]["humidity"]
                daily_forecasts[date].append({
                    "temperature": temperature,
                    "feels_like": feels_like,
                    "description": description,
                    "wind_speed": wind_speed,
                    "humidity": humidity
                })
            
            weather_summaries = []
            for date, forecasts in daily_forecasts.items():
                avg_temp = sum(f["temperature"] for f in forecasts) / len(forecasts)
                avg_feels_like = sum(f["feels_like"] for f in forecasts) / len(forecasts)
                descriptions = ", ".join(set(f["description"] for f in forecasts))
                avg_wind_speed = sum(f["wind_speed"] for f in forecasts) / len(forecasts)
                avg_humidity = sum(f["humidity"] for f in forecasts) / len(forecasts)
                weather_summary = f"""
                **Date**: {date}
                **Average Temperature**: {avg_temp:.2f}°C
                **Average Feels Like**: {avg_feels_like:.2f}°C
                **Descriptions**: {descriptions}
                **Average Wind Speed**: {avg_wind_speed:.2f} m/s
                **Average Humidity**: {avg_humidity:.2f}%
                """
                weather_summaries.append(weather_summary)
            
            result = {
                "city_name": city_name,
                "country": country,
                "weather_summaries": weather_summaries
            }
            return result
    except requests.exceptions.RequestException as e:
        st.error("Error occurred during API request")
        return {}

def generate_weather_image(weather_info):
    latest_forecast = weather_info['weather_summaries'][0]
    if not latest_forecast:
        return {"error": "No weather data available for the specified date and time"}

    prompt = f"""A view of {weather_info['city_name']} for a weather forecast with all the following information:
    {latest_forecast}"""

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return response.data[0].url
