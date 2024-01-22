from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import ChatCreateForm, MessageForm
from task_manager.models import Task, Worker, Position, TaskType, Message, Project, Team


def index(request: HttpRequest) -> HttpResponse:
    projects = Project.objects.count()
    tasks = Task.objects.count()
    teams = Team.objects.count()
    workers = Worker.objects.count()
    form = ChatCreateForm()
    context = {
        "tasks": tasks,
        "workers": workers,
        "projects": projects,
        "teams": teams,
        "form": form,
    }
    return render(request, "layouts/index.html", context)


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Message
    form_class = MessageForm
    template_name = "task_manager/task/task_detail.html"

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


class MessageDeleteView(LoginRequiredMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        task_pk = self.kwargs.get("task_pk")
        message_pk = self.kwargs.get("message_pk")
        message = get_object_or_404(Message, pk=message_pk)
        message.delete()
        return HttpResponseRedirect(
            reverse_lazy("task_manager:task_detail", args=[task_pk])
        )


class ChatCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = MessageForm

    def post(self, request, *args, **kwargs):
        task_id = request.POST.get("task")
        return HttpResponseRedirect(
            reverse_lazy("task_manager:task_detail", args=[task_id])
        )
