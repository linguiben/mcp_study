from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from .models.gemini import ask_gemini as ask_gemini
import sys

# # set http_proxy from ./.env file
# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8086'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8086'
# export HTTP_PROXY='http://localhost:8086' && export HTTPS_PROXY=${http_proxy}
sys.stdout.reconfigure(encoding='utf-8') 
server = MCPServerStreamableHTTP('http://JupiterSo.com:8001/mcp/')  
agent = Agent(ask_gemini.model, mcp_servers=[server])  

async def main():
    async with agent.run_mcp_servers():  
        print(agent.instrument)  # Print the system prompt
        result = await agent.run('How many days between 2000-01-01 and 2025-03-18?')
    print(result.output)
    #> There are 9,208 days between January 1, 2000, and March 18, 2025.

