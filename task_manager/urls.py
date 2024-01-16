from django.urls import path, include

from task_manager.views import (
    WorkerListView,
    TaskListView,
    TaskDetailView,
    MessageCreateView,
    WorkerDetailView,
    WorkerDeleteView,
    WorkerUpdateView,
    WorkerCreateView, TaskCreateView,
)

app_name = 'task_manager'
urlpatterns = [
    path("workers/", WorkerListView.as_view(), name="worker_list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker_detail"),
    path("workers/<int:pk>/delete", WorkerDeleteView.as_view(), name="worker_delete"),
    path("workers/<int:pk>/update", WorkerUpdateView.as_view(), name="worker_update"),
    path("workers/create", WorkerCreateView.as_view(), name="worker_create"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/create", TaskCreateView.as_view(), name="task_create"),

    path(
        "message/<int:pk_author>/<int:pk_task>",
        MessageCreateView.as_view(),
        name="message_create"
    ),

]
