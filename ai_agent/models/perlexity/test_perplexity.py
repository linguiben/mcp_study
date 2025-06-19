from perplexity import PerplexityModel
from pydantic_ai.chat import ChatSession

model = PerplexityModel(
    api_key="your-perplexity-api-key",
    base_url="https://api.perplexity.ai",
    model="pplx-7b-chat",  # or pplx-70b-chat
)

chat = ChatSession(model)

response = chat("请告诉我今天的天气如何？")
print(response.text)