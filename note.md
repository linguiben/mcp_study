```python
# main.py
import asyncio
import logging
from ai_agent import agent as agent
#logging.basicConfig(level=logging.DEBUG)
asyncio.run(agent.main())

# from ai_agent import agent_2 as agent
# asyncio.run(agent.main())

# promt = """ 
# 把图中的数据转成csv格式，第一行为标题行，标题行的内容为：
# indexName, indexValue, indexChange, indexChangeRate
# """

# import ai_agent.models.gemini.ask_gemini as ask_gemini

# ask_gemini.ask_gemini_with_image(
#     image_path="/Users/jupiter/16.vscode-workspace/mcp_study/data/202506192319_google_finance.png",
#     prompt=promt
# )
```
---
```python
# ai_agent/agent.py
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from .models.gemini import ask_gemini as ask_gemini
from .tools import tools as tools
import sys

# # set http_proxy from ./.env file
# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8086'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8086'
# export HTTP_PROXY='http://localhost:8086' && export HTTPS_PROXY=${http_proxy}
sys.stdout.reconfigure(encoding='utf-8')
# server = MCPServerStreamableHTTP('http://JupiterSo.com:8001/mcp/')
server = MCPServerStreamableHTTP('http://localhost:8000/mcp/')
agent = Agent(ask_gemini.model,
                system_prompt="You are an experienced programmer",
                tools=[tools.read_file, tools.list_files, tools.rename_file],
                mcp_servers=[server]
                )
async def main():
    async with agent.run_mcp_servers():
        print(agent.instrument)
        history = []
        while True:
            user_input = check_user_input(input("Input: "))
            # resp = agent.run_sync(user_input,
            resp = await agent.run(user_prompt=user_input,
                                message_history=history,
                                model_settings={"timeout": 60},
                                log_level="DEBUG"  # Set log level to DEBUG for detailed output
                                )
            history = list(resp.all_messages())
            # print("=== All Messages ===")
            # for msg in history:
            #     print(msg)
            # print("=== Output ===")
            print(resp.output)


def check_user_input(user_input: str) -> str:
    """
    if user intput "exit" or "quit', exit the program,
    otherwise return the user input.
    """
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        sys.exit()
    return user_input

if __name__ == "__main__":
    main()

```

```python
# ai_agent/models/gemini/ask_gemini.py
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8086'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8086'
load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')
model = ("gemini-2.0-flash-001")

def ask_gemin(contents: types.Content) -> str:
    """
    Ask Gemini model with the given prompt and return the response text.
    
    :param prompt: The input prompt to send to the Gemini model.
    :return: The response text from the Gemini model.
    """
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        # project="your-project-id",  # Replace with your actual project ID
        # location="global"  # Replace with your actual location if needed
    )
    generate_content_config = types.GenerateContentConfig(
        temperature = 1,
        top_p = 1,
        seed = 0,
        max_output_tokens = 8192
    )
    for chunk in client.models.generate_content_stream(
        model = model,
        contents = contents,
        config = generate_content_config,
    ):
        print(chunk.text, end='', flush=True)
        print()  # Ensure a newline after the response
    return chunk.text

def ask_gemini_with_image(image_path: str, prompt: str) -> str:
    """ 
    Ask Gemini model with an image and a prompt, and return the response text.
    :param image_path: The path to the image file to send to the Gemini model.  
    :param prompt: The input prompt to send to the Gemini model.
    :return: The response text from the Gemini model.
    """
    if prompt.__len__() < 10:
        return "Error: Prompt must be at least 10 characters long."
    try:
        if image_path is None or not image_path.strip():
            contents = [types.Content(role="user",parts=[types.Part(text=prompt)])]
            return ask_gemin(contents)
        if not os.path.exists(image_path):
            return f"Error: Image file '{image_path}' does not exist."
            # image = types.Image(
            #     uri="gs://your-bucket-name/your-image.jpg"  # Replace with your actual image URI
            # )
        image = types.Part.from_bytes(
            data=open(image_path, "rb").read(),
            mime_type="image/png"
        )
        contents = [
            types.Content(
                role="user",
                parts=[
                    image, 
                    types.Part(text=prompt)
                ]
            )
        ]
        return ask_gemin(contents)
    except Exception as e:
        print(f"Error: {e}")
        return str(e)

# from ai_agent.tools import rename_file, read_file, list_files
def persistent_session():
    """
    Main function to interact with the Gemini model.
    """
    while True:
        user_input = input("Input: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        response_text = ask_gemini_with_image("", user_input)
        print("Response:", response_text)

if __name__ == "__main__":
    persistent_session()
```
---
```python
# ai_agent/tools.py
from pathlib import Path
import os

# get the current directory of this file
base_dir = Path(__file__).parent.parent / "test" # __file__ is the path to this file

def read_file(name: str) -> str:
    """Return file content. If not exist, return error message.
    """
    print(f"(read_file {name})")
    try:
        with open(base_dir / name, "r") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"An error occurred: {e}"

def list_files() -> list[str]:
    print("(list_file)")
    file_list = []
    for item in base_dir.rglob("*"):
        if item.is_file():
            file_list.append(str(item.relative_to(base_dir)))
    return file_list

def rename_file(name: str, new_name: str) -> str:
    print(f"(rename_file {name} -> {new_name})")
    try:
        new_path = base_dir / new_name
        if not str(new_path).startswith(str(base_dir)):
            return "Error: new_name is outside base_dir."

        os.makedirs(new_path.parent, exist_ok=True)
        os.rename(base_dir / name, new_path)
        return f"File '{name}' successfully renamed to '{new_name}'."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    print(list_files())
    print(read_file("a"))
```