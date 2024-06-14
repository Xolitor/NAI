import openai
import os
from dotenv import load_dotenv
import time
import requests
import json
import streamlit as st
from collections import defaultdict

load_dotenv()

news_api_id = os.environ.get("NEWS_API_KEY")
weather_api_id = os.environ.get("WEATHER_API_KEY")
ass_id = os.environ.get("ASSISTANT_KEY")
client = openai.OpenAI()

model = "gpt-3.5-turbo-16k"

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

def main():
    st.set_page_config(page_title="NAI", page_icon=":books:", layout="centered")
    st.title("NAI: Your Personal Assistant")

    tab1, tab2, tab3 = st.tabs(["News", "Weather", "Weather Image"])

    with tab1:
        st.subheader("Get the latest news")
        news_topic = st.text_input("Enter the topic you want news about:")
        if st.button("Get News"):
            if news_topic:
                news = get_news(news_topic)
                if news:
                    for idx, article in enumerate(news, start=1):
                        st.markdown(f"**{idx}.** {article}")
                else:
                    st.warning("No news found for the given topic.")
            else:
                st.warning("Please enter a topic.")

    with tab2:
        st.subheader("Get the weather forecast")
        city = st.text_input("Enter the city:")
        if st.button("Get Weather"):
            if city:
                try:
                    weather_info = get_weather(city)
                    if weather_info:
                        for summary in weather_info["weather_summaries"]:
                            st.markdown(summary)
                    else:
                        st.error("Error fetching weather data.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a city.")

    with tab3:
        st.subheader("Generate Weather Image")
        city_for_image = st.text_input("Enter the city for the weather image:")
        if st.button("Generate Image"):
            if city_for_image:
                weather_info = get_weather(city_for_image)
                if weather_info:
                    image_url = generate_weather_image(weather_info)
                    if "error" not in image_url:
                        st.image(image_url)
                        st.write(weather_info['weather_summaries'][0])
                    else:
                        st.error(image_url["error"])
                else:
                    st.error("Error fetching weather data.")
            else:
                st.warning("Please enter a city.")

if __name__ == "__main__":
    main()
