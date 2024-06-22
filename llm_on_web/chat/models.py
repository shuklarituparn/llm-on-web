import uuid

from django.db import models

from llm_on_web.users.models import User

# Create your models here.


class Chatid(models.Model):
    chatid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chatid {self.chatid}"


class Conversations(models.Model):
    conversationid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    chatid = models.ForeignKey(
        Chatid,
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    userid = models.ForeignKey(User, on_delete=models.RESTRICT)
    llm_response = models.TextField(default="")
    user_query = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Conversation {self.conversationid} in chat {self.chatid} by {self.userid}"
        )
