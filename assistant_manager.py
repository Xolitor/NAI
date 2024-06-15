import openai
import os
import time
import json
import streamlit as st
from api_utils import get_news, get_weather

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"
ass_id = os.environ.get("ASSISTANT_KEY")

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
                final_string = "\n".join(output["weather_summaries"])
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
