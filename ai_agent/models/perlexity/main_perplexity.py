from pydantic_ai.models.openai import
from pydantic_ai import Agent

from dotenv import load_dotenv
import mcp_server.tools as tools

load_dotenv()
model = OpenAIModel("")

agent = Agent(model,
              system_prompt="You are an experienced programmer",
              tools=[tools.read_file, tools.list_files, tools.rename_file])

def main():
    history = []
    while True:
        user_input = input("Input: ")
        resp = agent.run_sync(user_input,
                              message_history=history)
        history = list(resp.all_messages())
        print(resp.output)


if __name__ == "__main__":
    main()
