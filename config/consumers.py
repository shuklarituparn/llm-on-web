import json
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer
from ollama import AsyncClient


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


async def chatllava(self, usermessage: str, image):
    conv_id = str(uuid.uuid4())
    async for response in await AsyncClient().generate(
        "bakllava",
        usermessage,
        images=[image],
        stream=True,
    ):
        responsefromllm = response["response"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": f"{responsefromllm}",
                    "done": response["done"],
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
        await chat(self, usermessage=data["message"])

    async def disconnect(self, code):
        await self.close()


class ChatUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await chat(self, usermessage=data["message"])

    async def disconnect(self, code):
        await self.close()


# Todo: Getting the correct data from the server
class ChatLlavaGConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        usermessage = data["message"]
        imagedata = data["imgDataToServer"]
        await chatllava(self, usermessage=usermessage, image=imagedata)

    async def disconnect(self, code):
        await self.close()


#  TODO: USE THE USER TEXT TO PROMPT AND THEN SEND THE RESPONSE BACK
class ChatLlavaUConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(
            text_data=json.dumps(
                {
                    "message": f"{text_data}",
                },
            ),
        )

    async def disconnect(self, code):
        await self.close()
