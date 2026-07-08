import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


class OpenAIBot:
    def __init__(self, engine):
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.engine = engine

    def add_message(self, role, content):
        self.conversation.append({"role": role, "content": content})

    def generate_response(self, prompt):
        self.add_message("user", prompt)
        try:
            response = client.chat.completions.create(
                model=self.engine,
                messages=self.conversation
            )
            
            assistant_response = response.choices[0].message.content.strip()

            self.add_message("assistant", assistant_response)
            return assistant_response
        except Exception as e:
            print(f"Error Generating Response! {e}")
            return "Error: Something went wrong while generating a response."