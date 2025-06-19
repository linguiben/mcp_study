from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai import Agent

from dotenv import load_dotenv
import tools.tools as tools
import os
import sys

load_dotenv()

# # set http_proxy from ./.env file
# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8086'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8086'
# export HTTP_PROXY='http://localhost:8086' && export HTTPS_PROXY=${http_proxy}
sys.stdout.reconfigure(encoding='utf-8') 

model = GeminiModel("gemini-2.0-flash-001")

agent = Agent(model,
              system_prompt="You are an experienced programmer",
              tools=[tools.read_file, tools.list_files, tools.rename_file])

def main():
    history = []
    while True:
        user_input = input("Input: ")
        resp = agent.run_sync(user_input,
                              message_history=history,
                              model_settings={"timeout": 60}
                              )
        history = list(resp.all_messages())
        print(resp.output)


if __name__ == "__main__":
    main()

