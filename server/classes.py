from pydantic import BaseModel
from typing import Literal


class SendMessage(BaseModel):
    model: str
    prompt: str


class ApiKey(BaseModel):
    server_url: str
    api_key: str


class SendPrompt(BaseModel):
    message: str


class LocalMCP(BaseModel):
    name: str
    transport: Literal["stdio"] = "stdio"
    command: str
    args: list[str] = []
    env: dict[str, str] = {}


class RemoteMCP(BaseModel):
    name: str
    transport: Literal["streamable-http"] = "streamable-http"
    url: str
    headers: dict[str, str] = {}
