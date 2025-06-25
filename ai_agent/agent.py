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

