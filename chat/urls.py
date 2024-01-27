from django.urls import path

from chat.views import (
    MessageCreateView,
    MessageDeleteView,
    ChatCreateView
)

app_name = "chat"
urlpatterns = [
    path(
        "message/<int:pk_author>/<int:pk_task>/",
        MessageCreateView.as_view(),
        name="message_create",
    ),
    path(
        "message/<int:message_pk>/<int:task_pk>/message_delete/",
        MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("chat/", ChatCreateView.as_view(), name="chat_create"),
]
