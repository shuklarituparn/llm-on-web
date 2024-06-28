from http import HTTPStatus

import ollama
from ollama import AsyncClient

model = "llama3"


async def modelcheck():
    try:
        ollama.chat(model)
    except ollama.ResponseError as e:
        if e.status_code == HTTPStatus.NOT_FOUND:
            ollama.pull(model)
            return False


async def chat(usermessage: str) -> str:
    usercontent = usermessage["message"]
    full_response = ""
    message = {"role": "user", "content": f"{usercontent}"}
    async for part in await AsyncClient().chat(
        model="llama3",
        messages=[message],
        stream=True,
    ):
        response = part["message"]["content"]
        full_response += response
