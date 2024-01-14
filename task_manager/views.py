from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from task_manager.models import Task, TaskType, Position, Worker


@login_required
def index(request: HttpRequest) -> HttpResponse:
    completed_tasks = Task.objects.filter(is_completed=True).count()
    uncompleted_tasks = Task.objects.filter(is_completed=False).count()
    workers = Worker.objects.count()
    positions = Position.objects.count()
    task_types = TaskType.objects.count()
    context = {
        "completed_tasks": completed_tasks,
        "uncompleted_tasks": uncompleted_tasks,
        "workers": workers,
        "positions": positions,
        "task_types": task_types,
    }
    return render(request, "index.html", context)
