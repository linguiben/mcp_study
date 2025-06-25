from pydantic_ai import Agent
agent = Agent("gemini-2.0-flash-001", 
            model_settings=dict(max_tokens=500))
resp = agent.run_sync("What is the capital of France?")
print(resp.output)