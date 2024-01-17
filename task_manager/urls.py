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
    TeamTaskAddView, TeamMemberAddView, TagListView,
    TagCreateView, TagDeleteView, TagUpdateView, TeamMemberDeleteView, TeamTaskDeleteView, ProjectListView,
    ProjectCreateView, ProjectDeleteView, ProjectUpdateView, ProjectTeamDeleteView,
    ProjectTaskDeleteView,
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
    path("tags/", TagListView.as_view(), name="tag_list"),
    path("tags/create/", TagCreateView.as_view(), name="tag_create"),
    path("tags/<int:pk>/delete/", TagDeleteView.as_view(), name="tag_delete"),
    path("tags/<int:pk>/update/", TagUpdateView.as_view(), name="tag_update"),

    path("projects/", ProjectListView.as_view(), name="project_list"),
    path("projects/create/", ProjectCreateView.as_view(), name="project_create"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project_update"),
    path(
        "projects/<int:project_pk>/<int:team_pk>/task_delete/",
        ProjectTeamDeleteView.as_view(),
        name="project_team_delete"
    ),
    path(
        "projects/<int:project_pk>/<int:task_pk>/member_delete/",
        ProjectTaskDeleteView.as_view(),
        name="project_task_delete"
    ),
]
