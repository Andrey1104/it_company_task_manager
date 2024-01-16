from django.urls import path

from task_manager.views import (
    WorkerListView,
    TaskListView,
    TaskDetailView,
    MessageCreateView,
    WorkerDetailView,
    WorkerDeleteView,
    WorkerUpdateView,
    WorkerCreateView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    TaskStatusUpdateView,
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamDeleteView,
    TeamUpdateView,
    TeamTaskDeleteView, TeamTaskAddView, TeamMemberDeleteView, TeamMemberAddView,
)

app_name = 'task_manager'
urlpatterns = [
    path("workers/", WorkerListView.as_view(), name="worker_list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker_detail"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker_delete"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker_update"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker_create"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/complete/", TaskStatusUpdateView.as_view(), name="task_status_update"),
    path("teams/", TeamListView.as_view(), name="team_list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team_detail"),
    path("teams/create/", TeamCreateView.as_view(), name="team_create"),
    path("teams/<int:pk>/delete/", TeamDeleteView.as_view(), name="team_delete"),
    path("teams/<int:pk>/update/", TeamUpdateView.as_view(), name="team_update"),
    path(
        "teams/<int:team_pk>/<int:task_pk>/task_delete/",
        TeamTaskDeleteView.as_view(),
        name="team_task_delete"
    ),
    path(
        "teams/<int:team_pk>/<int:member_pk>/member_delete/",
        TeamMemberDeleteView.as_view(),
        name="team_member_delete"
    ),
    path("teams/<int:pk>/team_task_add/", TeamTaskAddView.as_view(), name="team_task_add"),
    path("teams/<int:pk>/team_member_add/", TeamMemberAddView.as_view(), name="team_member_add"),

    path(
        "message/<int:pk_author>/<int:pk_task>/",
        MessageCreateView.as_view(),
        name="message_create"
    ),

]
