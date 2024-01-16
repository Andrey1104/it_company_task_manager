from django.contrib import admin
from django.urls import path, include
from task_manager.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", index, name="index"),
    path("task_manager/", include("task_manager.urls", namespace="task_manager")),
    path("accounts/", include("django.contrib.auth.urls")),
]
