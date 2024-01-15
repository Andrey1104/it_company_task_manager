from django.contrib import admin
from django.urls import path, include

from task_manager.views import WorkerListView

app_name = 'task_manager'
urlpatterns = [
    path("worker_list/", WorkerListView.as_view(), name="worker_list"),


]
