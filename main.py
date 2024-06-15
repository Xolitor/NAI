import streamlit as st
from assistant_manager import AssistantManager, AssistantRunFailedError
from config import set_page_config, set_custom_styles
from api_utils import get_weather, generate_weather_image

def main():
    manager = AssistantManager()
    set_page_config()
    set_custom_styles()
    st.markdown("<h1 class='title'>NAI: Your Personal Assistant</h1>", unsafe_allow_html=True)

    st.write("NAI offers two functionalities:")
    st.write("1. Get a list of news articles on a given topic")
    st.write("2. Get the weather forecast for a city and generate a weather image")

    tab1, tab2, tab3 = st.tabs(["📰 News", "🌤️ Weather", "🌥️ Weather Image"])

    with tab1:
        st.subheader("Get the Latest News")
        news_topic = st.text_input("Enter the topic you want news about:", key="news_input")
        if st.button("Get News", key="news_button"):
            if news_topic:
                try:
                    manager.create_assistant(
                        name="NAIv2",
                        instructions="""You are a personal assistant who can summarize news articles based on their titles and descriptions.""",
                        tools=[
                            {
                                "type": "function",
                                "function": {
                                    "name": "get_news",
                                    "description": "Get the list of articles/news for the given topic",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "topic": {
                                                "type": "string",
                                                "description": "The topic for which you want to get the news"
                                            }
                                        },
                                        "required": ["topic"],
                                    },
                                },
                            }
                        ]
                    )
                    manager.create_thread()

                    manager.create_message(
                        role="user",
                        content=f"Get news on {news_topic}"
                    )

                    manager.run_assistant()
                    manager.wait_for_run_completion()

                    summary = manager.get_summary()
                    st.markdown("<div class='card slide-in'><h4>Here are some news articles:</h4></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='card slide-in'><p>{summary}</p></div>", unsafe_allow_html=True)

                except AssistantRunFailedError:
                    st.error("Assistant run failed. Please try again later.")
            else:
                st.warning("Please enter a topic.")

    with tab2:
        st.subheader("Get the Weather Forecast")
        city = st.text_input("Enter the city:", key="weather_input")
        if st.button("Get Weather", key="weather_button"):
            if city:
                try:
                    manager.create_assistant(
                        name="NAIv2",
                        instructions="""You are a personal assistant who can provide weather summaries for the upcoming days.""",
                        tools=[
                            {
                                "type": "function",
                                "function": {
                                    "name": "get_weather",
                                    "description": "Get the weather forecast for a city for the upcoming 5 days",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "city": {
                                                "type": "string",
                                                "description": "The city for which you want to get the weather"
                                            }
                                        },
                                        "required": ["city"],
                                    },
                                },
                            }
                        ]
                    )
                    manager.create_thread()

                    manager.create_message(
                        role="user",
                        content=f"Get weather for {city}"
                    )

                    manager.run_assistant()
                    manager.wait_for_run_completion()

                    summary = manager.get_summary()
                    st.markdown(f"<div class='card slide-in'><h4>Here is the weather forecast for {city}:</h4></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='card slide-in'><p>{summary}</p></div>", unsafe_allow_html=True)

                except AssistantRunFailedError:
                    st.error("Assistant run failed. Please try again later.")
            else:
                st.warning("Please enter a city.")

    with tab3:
        st.subheader("Generate Weather Image")
        city_image = st.text_input("Enter the city:", key="weather_image_input")
        if st.button("Generate Weather Image", key="weather_image_button"):
            if city_image:
                weather_info = get_weather(city_image)
                if weather_info:
                    image_url = generate_weather_image(weather_info)
                    if "error" not in image_url:
                        st.image(image_url)
                        st.markdown(f"<div class='card slide-in'><p>{weather_info['weather_summaries'][0]}</p></div>", unsafe_allow_html=True)
                    else:
                        st.error(image_url["error"])
                else:
                    st.error("Error fetching weather data.")
            else:
                st.warning("Please enter a city.")

if __name__ == "__main__":
    main()
