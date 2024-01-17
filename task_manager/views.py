
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
    TaskUpdateForm, TeamCreateForm, TeamTaskAddForm, TeamMemberAddForm, TagCreateForm
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
    return render(request, "layouts/index.html", context)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 3
    queryset = Worker.objects.select_related("position")
    template_name = "task_manager/worker/worker_list.html"


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "task_manager/worker/worker_detail.html"


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    template_name = "task_manager/worker/worker_form.html"


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "task_manager/worker/worker_form.html"
    success_url = reverse_lazy("task_manager:worker_list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "task_manager/worker/worker_delete.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 3
    template_name = "task_manager/task/task_list.html"
    queryset = (
        Task.objects
        .select_related("task_type")
        .prefetch_related("assignees", "teams")
    )


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    form_class = MessageForm
    template_name = "task_manager/task/task_detail.html"

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
    template_name = "task_manager/task/task_form.html"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("task_manager:task_list")
    template_name = "task_manager/task/task_form.html"


class TaskDeleteView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/task/task_delete.html"


class TaskStatusUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "task_manager/task/task_form.html"

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


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    queryset = Team.objects.all().prefetch_related("member", "task")
    template_name = "task_manager/team/team_list.html"


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    template_name = "task_manager/team/team_detail.html"


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamCreateForm
    template_name = "task_manager/task/task_form.html"
    success_url = reverse_lazy("task_manager:team_list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"
    template_name = "task_manager/team/team_form.html"


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    template_name = "task_manager/team/team_form.html"


class TeamActionMixin:
    @staticmethod
    def remove_object(team_id, object_id, team_attribute, object_model):
        team = get_object_or_404(Team, pk=team_id)
        obj = get_object_or_404(object_model, pk=object_id)

        if obj in getattr(team, team_attribute).all():
            getattr(team, team_attribute).remove(obj)
            team.save()

    @staticmethod
    def get_success_url(team_id):
        return reverse_lazy("task_manager:team_detail", args=[team_id])


class TeamTaskDeleteView(LoginRequiredMixin, TeamActionMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get("team_pk")
        self.remove_object(team_id, kwargs.get("task_pk"), "task", Task)
        return HttpResponseRedirect(self.get_success_url(team_id))


class TeamMemberDeleteView(LoginRequiredMixin, TeamActionMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get("team_pk")
        self.remove_object(team_id, kwargs.get("member_pk"), "member", Worker)
        return HttpResponseRedirect(self.get_success_url(team_id))


class TeamTaskAddView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamTaskAddForm
    template_name = "task_manager/team/team_form.html"


class TeamMemberAddView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamMemberAddForm
    template_name = "task_manager/team/team_form.html"


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 4
    template_name = "task_manager/tag/tag_list.html"


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag
    template_name = "task_manager/tag/tag_detail.html"


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    form_class = TagCreateForm
    template_name = "task_manager/tag/tag_form.html"
    success_url = reverse_lazy("task_manager:tag_list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    template_name = "task_manager/tag/tag_form.html"


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    template_name = "task_manager/tag/tag_delete.html"


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 4
    template_name = "task_manager/project/project_list.html"


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = "task_manager/project/project_detail.html"


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = TagCreateForm
    template_name = "task_manager/project/project_form.html"
    success_url = reverse_lazy("task_manager:")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"
    template_name = "task_manager/project/project_form.html"


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    template_name = "task_manager/project/project_delete.html"
