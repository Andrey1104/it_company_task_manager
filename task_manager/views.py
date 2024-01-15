from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import MessageForm
from task_manager.models import Task, TaskType, Position, Worker, Message


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
    return render(request, "task_manager/index.html", context)


class WorkerListView(generic.ListView):
    model = Worker

    def get_context_data(self, **kwargs) -> dict:
        context = super(WorkerListView, self).get_context_data(**kwargs)
        # username = self.request.GET.get("username", "")
        # context["search_form"] = WorkerSearchForm(
        #     initial={"username": username}
        # )
        return context


class TaskListView(generic.ListView):
    model = Task

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)
        # username = self.request.GET.get("username", "")
        # context["search_form"] = TaskSearchForm(
        #     initial={"username": username}
        # )
        context["tasks"] = Task.objects.select_related("task_type").prefetch_related("assignees")
        return context


class TaskDetailView(generic.DetailView):
    model = Task
    form_class = MessageForm


class MessageCreateView(generic.CreateView):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        author_pk = self.kwargs.get("author_pk")
        task_pk = self.kwargs.get("task_pk")
        author = Worker.objects.get(pk=author_pk)
        task = Task.objects.get(pk=task_pk)
        Message.objects.create(
            author=author,
            task=task,
            text=self.request.POST.get("text")
        )
        return HttpResponseRedirect(reverse_lazy(
            "task_manager:task_detail",
            args=[task.id]
        ))
