import openai
import os
from dotenv import load_dotenv
import time
import requests
import json
import streamlit as st

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

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api_id}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            city_name = data["city"]["name"]
            country = data["city"]["country"]
            weather_forecasts = []
            for forecast in data["list"][:5]:
                date_time = forecast["dt_txt"]
                temperature = forecast["main"]["temp"]
                feels_like = forecast["main"]["feels_like"]
                description = forecast["weather"][0]["description"]
                wind_speed = forecast["wind"]["speed"]
                humidity = forecast["main"]["humidity"]
                weather_forecast = f"""
                **Date/Time**: {date_time}
                **Temperature**: {temperature}°C
                **Feels Like**: {feels_like}°C
                **Description**: {description}
                **Wind Speed**: {wind_speed} m/s
                **Humidity**: {humidity}%
                """
                weather_forecasts.append(weather_forecast)
            result = {
                "city_name": city_name,
                "country": country,
                "weather_forecasts": weather_forecasts
            }
            return result
    except requests.exceptions.RequestException as e:
        st.error("Error occurred during API request")
        return {}

def generate_weather_image(weather_info):
    latest_forecast = weather_info['weather_forecasts'][0]
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

class AssistantRunFailedError(Exception):
    pass

class AssistantManager:
    thread_id = None
    assistant_id = ass_id

    def __init__(self, model: str = model) -> None:
        self.client = client
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.messages = None
        self.summary = None

        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id=AssistantManager.assistant_id)

        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(thread_id=AssistantManager.thread_id)

    def create_assistant(self, name, instructions, tools):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                model=self.model,
                tools=tools
            )
            self.assistant = assistant_obj
            AssistantManager.assistant_id = assistant_obj.id

    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj

    def create_message(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role=role,
                content=content
            )

    def run_assistant(self):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant_id
            )

    def process_message(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            summary = []

            last_message = messages.data[0]
            response = last_message.content[0].text.value
            role = last_message.role
            summary.append(response)
            self.summary = "\n".join(summary)

    def call_required_functions(self, required_actions):
        if not self.run:
            return
        tool_outputs = []

        for action in required_actions["tool_calls"]:
            func_name = action["function"]["name"]
            arguments = json.loads(action["function"]["arguments"])

            if func_name == "get_news":
                output = get_news(topic=arguments["topic"])
                final_string = "\n".join(output)
                tool_outputs.append({"tool_call_id": action["id"], "output": final_string})

            elif func_name == "get_weather":
                output = get_weather(city=arguments["city"])
                final_string = "\n".join(output["weather_forecasts"])
                tool_outputs.append({"tool_call_id": action["id"], "output": final_string})

            else:
                raise ValueError(f"Function {func_name} not found")

        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=self.run.id,
            tool_outputs=tool_outputs
        )

    def get_summary(self):
        return self.summary

    def wait_for_run_completion(self):
        if self.thread and self.run:
            with st.spinner("Wait... Generating response..."):
                while True:
                    time.sleep(5)
                    run_status = self.client.beta.threads.runs.retrieve(
                        thread_id=self.thread.id,
                        run_id=self.run.id
                    )

                    if run_status.status == "completed":
                        self.process_message()
                        break
                    elif run_status.status == "requires_action":
                        self.call_required_functions(required_actions=run_status.required_action.submit_tool_outputs.model_dump())

                    elif run_status.status == "failed":
                        raise AssistantRunFailedError("Assistant run failed")

                    elif run_status.status == "stopped":
                        break

    def run_steps(self):
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=self.thread.id,
            run_id=self.run.id
        )
        return run_steps.data

def main():
    manager = AssistantManager()
    st.set_page_config(page_title="NAI", page_icon=":books:", layout="centered")
    st.title("NAI: Your personal Assistant")

    st.write("NAI has 2 functionalities:")
    st.write("1. Ask for a list of news articles on a given topic")
    st.write("2. Ask for the weather forecast of a city")

    tab1, tab2 = st.tabs(["News", "Weather"])

    with tab1:
        st.subheader("Get the latest news")
        news_topic = st.text_input("Enter the topic you want news about:")
        if st.button("Get News"):
            if news_topic:
                try:
                    manager.create_assistant(
                        name="NAIv2",
                        instructions="""You are a personal Assistant who knows how to take a list of article's titles and descriptions and then write a short summary of all the news articles.""",
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
                    st.write(summary)

                except AssistantRunFailedError:
                    st.error("Assistant run failed. Please try again later.")
            else:
                st.warning("Please enter a topic.")

    with tab2:
        st.subheader("Get the weather forecast")
        city = st.text_input("Enter the city:")
        if st.button("Get Weather"):
            if city:
                try:
                    manager.create_assistant(
                        name="NAIv2",
                        instructions="""You are a personal Assistant who knows how to take a list of weather forecasts and then provide a summary of the weather for the upcoming days.""",
                        tools=[
                            {
                                "type": "function",
                                "function": {
                                    "name": "get_weather",
                                    "description": "Get the weather forecast of a city in the upcoming 5 days",
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
                    st.write(summary)

                except AssistantRunFailedError:
                    st.error("Assistant run failed. Please try again later.")
            else:
                st.warning("Please enter a city.")

        if st.button("Generate Weather Image"):
            if city:
                weather_info = get_weather(city)
                if weather_info:
                    image_url = generate_weather_image(weather_info)
                    if "error" not in image_url:
                        st.image(image_url)
                        st.write(weather_info['weather_forecasts'][0])
                    else:
                        st.error(image_url["error"])
                else:
                    st.error("Error fetching weather data.")
            else:
                st.warning("Please enter a city.")

if __name__ == "__main__":
    main()
