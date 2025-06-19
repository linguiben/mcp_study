from pydantic_ai import Agent
from .models.gemini import ask_gemini as ask_gemini
from .models.gemini import ask_gemini as ask_gemini_with_image
from .tools import tools as tools
import sys

# # set http_proxy from ./.env file
# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8086'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8086'
# export HTTP_PROXY='http://localhost:8086' && export HTTPS_PROXY=${http_proxy}
sys.stdout.reconfigure(encoding='utf-8') 
agent = Agent(ask_gemini.model,
                system_prompt="You are an experienced programmer",
                tools=[tools.read_file, tools.list_files, tools.rename_file])
def main():
    history = []
    while True:
        user_input = check_user_input(input("Input: "), history)
        if not user_input: # if user_input is None or empty string
            continue
        resp = agent.run_sync(user_input,
                              message_history=history,
                              model_settings={"timeout": 60}
                              )
        history = list(resp.all_messages())
        print(resp.output)

def check_user_input(user_input: str, history: str) -> str:
    """
    if user intput "exit" or "quit', exit the program,
    otherwise return the user input.
    if user input "clear" or "cls", clear the history.
    """
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        sys.exit()
    elif user_input.lower() in ["clear", "cls"]:
        print("Clearing history...")
        history.clear()
        return ""
    return user_input

if __name__ == "__main__":
    main()

