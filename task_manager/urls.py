from django.contrib import admin
from django.urls import path, include

from task_manager.views import (
    WorkerListView,
    TaskListView,
    TaskDetailView,
)

app_name = 'task_manager'
urlpatterns = [
    path("workers/", WorkerListView.as_view(), name="worker_list"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),

]