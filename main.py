import openai
import os
from dotenv import find_dotenv, load_dotenv
import time
import logging
import requests
import json
import streamlit as st
from datetime import datetime

load_dotenv()

news_api_id = os.environ.get("NEWS_API_KEY")
client = openai.OpenAI()

model = "gpt-3.5-turbo-16k"

def get_news(topic):
    url =(
        f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_id}"
        )
    try:
        response = requests.get(url)
        if response.status_code == 200:
            news = json.dumps(response.json(), indent=4)
            news_json = json.loads(news)
            data = news_json
            
            #Access all the fields in the JSON response
            status = data["status"]
            total_results = data["totalResults"]
            articles = data["articles"]
            final_news = []
            
            for article in articles:
                title = article["title"]
                description = article["description"]
                source_name = article["source"]["name"]
                url = article["url"]
                author = article["author"]
                content = article["content"]
                title_description = f"""
                        Title: {title},
                        Author: {author},,
                        Source: {source_name},
                        Description: {description},
                        URL: {url},
                """
                final_news.append(title_description)
            return final_news 
    
    except requests.exceptions.RequestException as e:
        print("Error occured during API request", e)
    
class AssistantRunFailedError(Exception):
        pass
    
class AssistantManager:
    thread_id = None
    assisstant_id = "asst_akXuAr41x3T9oacZ9RUSbJHw"
    
    def __init__(self, model: str = model) -> None:
        self.client = client
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.messages = None
        self.summary = None
        
        # Retrieve existing assistant and thread if IDs are already created
        
        if AssistantManager.assisstant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id=AssistantManager.assisstant_id)
            
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
            AssistantManager.assisstant_id = assistant_obj.id
            print(assistant_obj)
            
    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            print(thread_obj)
            
    def create_message(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role=role,
                content=content
            )
            
    def run_assistant(self, instructions):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assisstant_id,
                instructions=instructions
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
            print(f"SUMMARY----->{role.capitalize()}: ==> {response}")
            
    def call_required_functions(self, required_actions):
        if not self.run:
            return
        tool_outputs = []
        
        for action in required_actions["tool_calls"]:
            func_name = action["function"]["name"]
            arguments = json.loads(action["function"]["arguments"])
            
            if func_name == "get_news":
                output = get_news(topic=arguments["topic"])
                print(f"STUFFFF;;;;{output}")
                final_string = ""
                for item in output:
                    final_string += "".join(item)
                tool_outputs.append({"tool_call_id":action["id"], "output":final_string})
            else:
                raise ValueError(f"Function {func_name} not found")
            
        print("Submitiing output back to the Assisstant")
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=self.run.id,
            tool_outputs=tool_outputs
            )
        
    # for streamlit
    def get_summary(self):
        return self.summary
            
    def wait_for_run_completion(self):
            if self.thread and self.run:
                while True:
                    time.sleep(5)
                    run_status = self.client.beta.threads.runs.retrieve(
                        thread_id=self.thread.id,
                        run_id=self.run.id
                        )
                    print(f"Run Status: {run_status.model_dump_json(indent=4)}")
                    
                    if run_status.status == "completed":
                        self.process_message()
                        break
                    elif run_status.status == "requires_action":
                        print("Run requires action")
                        self.call_required_functions(required_actions=run_status.required_action.submit_tool_outputs.model_dump())
                        
                    elif run_status.status == "failed":
                        print("Run failed")
                        raise AssistantRunFailedError("Assistant run failed")
                    
                    elif run_status.status == "stopped":
                        print("Run stopped")
                        break
                    
    def run_steps(self):
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=self.thread.id,
            run_id=self.run.id
            )
        print(f"Run Steps---> {run_steps}")
        return run_steps.data   



def main():
    #bitcoin_news = get_news("Israel")
    #print(bitcoin_news[0])
    manager = AssistantManager()
    
    st.title("NAI: Your personal news article summarizer Assistant")
    
    with st.form(key="user_input_form"):
        instructions = st.text_input("Enter topic: ")
        submit_button = st.form_submit_button(label="Run NAI")  
        
        if submit_button:
            try:
                manager.create_assistant(
                    name="NAI",
                    instructions="You are a personal article summarizer Assistant who knows how to take a list of article's titles and descriptions and then write a short summary of all the news articles ",
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
                    ],
                )
                manager.create_thread()
                
                manager.create_message(
                    role="user",
                    content=f"summarize the news on this topic: {instructions}?"
                )
                
                manager.run_assistant(instructions="summarize the news on this topic")
                
                manager.wait_for_run_completion()
                
                summary = manager.get_summary()
                
                st.write(summary)
                st.text("Run steps:")
                st.code(manager.run_steps(), line_numbers=True) 
                
            except AssistantRunFailedError:
                st.error("Assistant run failed. Please try again later.")
        
        
if __name__ == "__main__":
    main()
