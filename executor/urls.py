from django.urls import path

from executor.views.project_views import (
    ProjectListView,
    ProjectCreateView,
    ProjectDeleteView,
    ProjectUpdateView,
    ProjectTeamDeleteView,
    ProjectTaskDeleteView,
)
from executor.views.team_views import (
    TeamListView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
    TeamTaskDeleteView,
    TeamMemberDeleteView,
    TeamTaskAddView,
    TeamMemberAddView,
)
from executor.views.worker_views import (
    WorkerListView,
    WorkerDetailView,
    WorkerDeleteView,
    WorkerUpdateView,
    WorkerCreateView,
    WorkerTaskAddView,
    WorkerTaskDeleteView,
)

app_name = "executor"
urlpatterns = [
    path("workers/", WorkerListView.as_view(), name="worker_list"),
    path(
        "workers/<int:pk>/", WorkerDetailView.as_view(), name="worker_detail"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker_delete",
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker_update",
    ),
    path("workers/create/", WorkerCreateView.as_view(), name="worker_create"),
    path(
        "workers/<int:pk>/worker_task_add/",
        WorkerTaskAddView.as_view(),
        name="worker_task_add",
    ),
    path(
        "workers/<int:worker_pk>/<int:task_pk>/task_delete/",
        WorkerTaskDeleteView.as_view(),
        name="worker_task_delete",
    ),
    path("teams/", TeamListView.as_view(), name="team_list"),
    path("teams/create/", TeamCreateView.as_view(), name="team_create"),
    path(
        "teams/<int:pk>/update/", TeamUpdateView.as_view(), name="team_update"
    ),
    path(
        "teams/<int:pk>/delete/", TeamDeleteView.as_view(), name="team_delete"
    ),
    path(
        "teams/<int:team_pk>/<int:task_pk>/task_delete/",
        TeamTaskDeleteView.as_view(),
        name="team_task_delete",
    ),
    path(
        "teams/<int:team_pk>/<int:member_pk>/member_delete/",
        TeamMemberDeleteView.as_view(),
        name="team_member_delete",
    ),
    path(
        "teams/<int:pk>/team_task_add/",
        TeamTaskAddView.as_view(),
        name="team_task_add",
    ),
    path(
        "teams/<int:pk>/team_member_add/",
        TeamMemberAddView.as_view(),
        name="team_member_add",
    ),
    path("projects/", ProjectListView.as_view(), name="project_list"),
    path(
        "projects/create/", ProjectCreateView.as_view(), name="project_create"
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project_delete",
    ),
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project_update",
    ),
    path(
        "projects/<int:project_pk>/<int:team_pk>/task_delete/",
        ProjectTeamDeleteView.as_view(),
        name="project_team_delete",
    ),
    path(
        "projects/<int:project_pk>/<int:task_pk>/member_delete/",
        ProjectTaskDeleteView.as_view(),
        name="project_task_delete",
    ),
]
