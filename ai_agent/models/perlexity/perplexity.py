# your_models/perplexity.py

from typing import List, Optional, Union, Dict, Any
from pydantic_ai.base import ChatModel
from pydantic_ai.message import ChatMessage
import httpx


class PerplexityModel(ChatModel):
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.perplexity.ai",
        model: str = "pplx-7b-chat",
        temperature: float = 0.7,
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model_name = model
        self.temperature = temperature
        self.timeout = timeout

    def _build_payload(self, messages: List[ChatMessage]) -> Dict[str, Any]:
        return {
            "model": self.model_name,
            "messages": [m.dict() for m in messages],
            "temperature": self.temperature,
        }

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat(
        self,
        messages: List[ChatMessage],
        functions: Optional[List[Dict[str, Any]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
    ) -> ChatMessage:
        payload = self._build_payload(messages)
        url = f"{self.base_url}/v1/chat/completions"

        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(url, headers=self._headers(), json=payload)
            resp.raise_for_status()
            data = resp.json()

        reply = data["choices"][0]["message"]
        return ChatMessage(role=reply["role"], content=reply["content"])
    