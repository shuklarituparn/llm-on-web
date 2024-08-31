from django.urls import path

from .views import user_conversations_detailed_view
from .views import user_conversations_view
from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("<int:pk>/conversations/", view=user_conversations_view, name="conversations"),
    path(
        "conversations/<uuid:conversationid>/",
        view=user_conversations_detailed_view,
        name="conversation_detail",
    ),
]
