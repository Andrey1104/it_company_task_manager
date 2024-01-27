from django.urls import path

from task.views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    TaskStatusUpdateView,
    TagListView,
    TagCreateView,
    TagDeleteView,
    TagUpdateView
)

app_name = "task"
urlpatterns = [

    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path(
        "tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"
    ),
    path(
        "tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"
    ),
    path(
        "tasks/<int:pk>/complete/",
        TaskStatusUpdateView.as_view(),
        name="task_status_update",
    ),

    path("tags/", TagListView.as_view(), name="tag_list"),
    path("tags/create/", TagCreateView.as_view(), name="tag_create"),
    path("tags/<int:pk>/delete/", TagDeleteView.as_view(), name="tag_delete"),
    path("tags/<int:pk>/update/", TagUpdateView.as_view(), name="tag_update"),
]
