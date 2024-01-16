from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from it_company_task_manager import settings
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


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker

    def get_context_data(self, **kwargs) -> dict:
        context = super(WorkerListView, self).get_context_data(**kwargs)
        # username = self.request.GET.get("username", "")
        # context["search_form"] = WorkerSearchForm(
        #     initial={"username": username}
        # )
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)
        # username = self.request.GET.get("username", "")
        # context["search_form"] = TaskSearchForm(
        #     initial={"username": username}
        # )
        context["tasks"] = Task.objects.select_related("task_type").prefetch_related("assignees")
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    form_class = MessageForm

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context["message_form"] = MessageForm()
        return context


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Message
    form_class = MessageForm
    template_name = "task_manager/task_detail.html"

    def form_valid(self, form: MessageForm) -> HttpResponse:
        author_pk = self.kwargs.get("pk_author")
        task_pk = self.kwargs.get("pk_task")

        author = get_object_or_404(Worker, pk=author_pk)
        task = get_object_or_404(Task, pk=task_pk)

        form.instance.author = author
        form.instance.task = task
        return super().form_valid(form)

    def get_success_url(self):
        task_pk = self.kwargs.get("pk_task")
        return reverse_lazy("task_manager:task_detail", args=[task_pk])
