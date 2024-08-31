import uuid

from django.db import models

from llm_on_web.users.models import User


class Chatid(models.Model):
    chatid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chat_title = models.CharField(max_length=255, default="", blank=True)
    userid = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return f"Chats: {self.userid}"


class Conversations(models.Model):
    conversationid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    chatid = models.ForeignKey(
        Chatid,
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    userid = models.ForeignKey(User, on_delete=models.RESTRICT)
    llm_response = models.TextField(max_length=1000, default="", blank=True)
    user_query = models.TextField(default="")
    imagequery = models.ImageField(
        upload_to="user-images-query/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Conversation {self.conversationid} in chat {self.chatid} by {self.userid}"
        )
