import base64
import json
import uuid

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile
from ollama import AsyncClient


async def chat(self, usermessage: str, pk):
    message = {"role": "user", "content": f"{usermessage}"}
    conv_id = str(uuid.uuid4())
    responsellm = ""
    async for part in await AsyncClient(host="http://host.docker.internal:11434/").chat(
        model="llama3",
        messages=[message],
        stream=True,
    ):
        response = part["message"]["content"]
        responsellm += response
        await self.send(
            text_data=json.dumps(
                {
                    "message": f"{response}",
                    "done": part["done"],
                    "conv_id": conv_id,
                },
            ),
        )
    return responsellm


async def chatllava(self, usermessage: str, image: str, pk):
    conv_id = str(uuid.uuid4())
    responsellm_llava = ""
    async for response in await AsyncClient(
        host="http://host.docker.internal:11434/",
    ).generate(
        "bakllava",
        usermessage,
        images=[image],
        stream=True,
    ):
        responsefromllava = response["response"]
        responsellm_llava += responsefromllava
        await self.send(
            text_data=json.dumps(
                {
                    "message": f"{responsefromllava}",
                    "done": response["done"],
                    "conv_id": conv_id,
                },
            ),
        )
    return responsellm_llava


class ChatGuestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await chat(self, usermessage=data["message"], pk=data["id"])

    async def disconnect(self, code):
        pass


class ChatUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        responsefromllm = await chat(self, usermessage=data["message"], pk=data["id"])
        await create_conversations(
            data["id"],
            responsefromllm,
            data["message"],
            "llama",
            None,
        )

    async def disconnect(self, code):
        pass


class ChatLlavaGConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        usermessage = data["message"]
        pk = data["id"]
        imagedata = data["imgDataToServer"]
        await chatllava(self, usermessage=usermessage, image=imagedata, pk=pk)

    async def disconnect(self, code):
        pass


class ChatLlavaUConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        usermessage = data["message"]
        imagedata = data["imgDataToServer"]
        base64imagedata = data["base64imagedata"]
        responsellm_llava = await chatllava(
            self,
            usermessage=usermessage,
            image=imagedata,
            pk=data["id"],
        )
        await create_conversations(
            data["id"],
            responsellm_llava,
            data["message"],
            "bakllava",
            image=base64imagedata,
        )

    async def disconnect(self, code):
        pass


@database_sync_to_async
def create_conversations(pk, responsellm, usermessage, model, image):
    from llm_on_web.chat.models import Chatid
    from llm_on_web.chat.models import Conversations
    from llm_on_web.users.models import User

    user = User.objects.get(pk=pk)
    user_chat_id = user.currentchatid
    chat_id_instance = Chatid.objects.get(chatid=user_chat_id)
    conversation_data = {
        "chatid": chat_id_instance,
        "llm_response": responsellm,
        "user_query": usermessage,
        "userid_id": pk,
    }
    if model == "bakllava" and image:
        imgformat, imagedata = image.split(";base64,")
        imagedata += "===="
        imageformat = imgformat.split("/")[-1]
        imagecontent = ContentFile(
            base64.standard_b64decode(imagedata),
            name=f"{uuid.uuid4()!s}.{imageformat}",
        )
        conversation_data["imagequery"] = imagecontent

    Conversations.objects.create(**conversation_data)
