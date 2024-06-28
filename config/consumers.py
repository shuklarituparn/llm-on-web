import json
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer
from ollama import AsyncClient

import llm.llm_chat as llmchat


async def chat(self, usermessage: str):
    message = {"role": "user", "content": f"{usermessage}"}
    conv_id = str(uuid.uuid4())
    async for part in await AsyncClient().chat(
        model="llama3",
        messages=[message],
        stream=True,
    ):
        response = part["message"]["content"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": f"{response}",
                    "done": part["done"],
                    "conv_id": conv_id,
                },
            ),
        )


# print(self.scope['user'])  so this reaches every class
class ChatGuestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if await llmchat.modelcheck() is False:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": "No LLM models installed, we'll fix it for you",
                    },
                ),
            )
        else:
            await chat(self, usermessage=data["message"])

    async def disconnect(self, code):
        await self.close()


class ChatUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if await llmchat.modelcheck() is False:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": "No LLM models installed, we'll fix it for you",
                    },
                ),
            )
        else:
            await chat(self, usermessage=data["message"])

    async def disconnect(self, code):
        await self.close()


class ChatLlavaGConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def disconnect(self, code):
        await self.close()


class ChatLlavaUConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data="Connection Made")

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def disconnect(self, code):
        await self.close()
