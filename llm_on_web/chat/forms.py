from llm_on_web.chat.models import Conversations


class UserConversationForm:
    class Meta:
        model = Conversations
        fields = ["userid", "user_query", "imagequery"]
