from django.contrib import admin
from django.urls import path, include

from chat.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", index, name="index"),
    path(
        "task/",
        include("task.urls", namespace="task"),
    ),
    path(
        "executor/",
        include("executor.urls", namespace="executor"),
    ),
    path(
        "chat/",
        include("chat.urls", namespace="chat"),
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]
