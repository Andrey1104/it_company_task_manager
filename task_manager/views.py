
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic


from task_manager.forms import (
    MessageForm,
    WorkerCreateForm,
    WorkerUpdateForm,
    TaskCreateForm,
    TaskUpdateForm, TeamCreateForm, TeamTaskAddForm, TeamMemberAddForm
)
from task_manager.models import (
    Task,
    TaskType,
    Position,
    Worker,
    Message,
    Tag,
    Project,
    Team
)


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
    paginate_by = 3
    queryset = Worker.objects.select_related("position")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker_list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 3
    queryset = (
        Task.objects
        .select_related("task_type")
        .prefetch_related("assignees")
    )


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    form_class = MessageForm

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        task = self.get_object()
        messages = task.messages.select_related()
        context["messages"] = messages
        context["message_form"] = MessageForm()
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("task_manager:task_list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("task_manager:task_list")


class TaskDeleteView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskStatusUpdateView(LoginRequiredMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        task = Task.objects.get(pk=task_id)
        if not task.is_completed:
            task.is_completed = True
        else:
            task.is_completed = False
        task.save()
        return HttpResponseRedirect(reverse_lazy(
            "task_manager:task_detail",
            args=[task_id]
        ))


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


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    queryset = Team.objects.all().prefetch_related("member", "task")


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy("task_manager:team_list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team


class TeamTaskDeleteView(LoginRequiredMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get("team_pk")
        task_id = kwargs.get("task_pk")
        team = Team.objects.get(pk=team_id)
        task = Task.objects.get(pk=task_id)
        if task in team.task.all():
            team.task.remove(task)
            team.save()

        return HttpResponseRedirect(reverse_lazy(
            "task_manager:team_detail",
            args=[team_id]
        ))


class TeamTaskAddView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamTaskAddForm

    def get_success_url(self):
        team_id = self.object.id
        return reverse_lazy("task_manager:team_detail", args=[team_id])


class TeamMemberDeleteView(LoginRequiredMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get("team_pk")
        member_id = kwargs.get("member_pk")
        team = Team.objects.get(pk=team_id)
        member = Worker.objects.get(pk=member_id)
        if member in team.member.all():
            team.member.remove(member)
            team.save()

        return HttpResponseRedirect(reverse_lazy(
            "task_manager:team_detail",
            args=[team_id]
        ))


class TeamMemberAddView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamMemberAddForm

    def get_success_url(self):
        team_id = self.object.id
        return reverse_lazy("task_manager:team_detail", args=[team_id])
