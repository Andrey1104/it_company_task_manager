
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from task_manager.forms import (
    MessageForm,
    WorkerCreateForm,
    WorkerUpdateForm,
    TaskCreateForm,
    TaskUpdateForm, TeamCreateForm, TeamTaskAddForm, TeamMemberAddForm, TagCreateForm,
    ProjectSearchForm, TagSearchForm, TeamSearchForm, TaskSearchForm, WorkerSearchForm, ProjectForm, WorkerTaskAddForm,

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


class ModelDeleteMixin:
    @staticmethod
    def remove_object(model_id, object_id, attribute, main_model, object_model):
        model = get_object_or_404(main_model, pk=model_id)
        obj = get_object_or_404(object_model, pk=object_id)

        if obj in getattr(model, attribute).all():
            getattr(model, attribute).remove(obj)
            model.save()

    @staticmethod
    def get_success_url(model_id=None):
        if model_id:
            return reverse_lazy("task_manager:team_detail", args=[model_id])
        return reverse_lazy("task_manager:project_list")


class SearchMixin:
    search_form_class = None
    search_fields = []

    @staticmethod
    def get_search_form_kwargs():
        return {}

    def get_search_query(self):
        return self.request.GET.get("name", "")

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.get_search_query()
        if search_query:
            for field in self.search_fields:
                queryset = queryset.filter(**{f"{field}__icontains": search_query})
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = self.search_form_class(
            initial={"name": self.get_search_query()},
            **self.get_search_form_kwargs()
        )
        context["search_form"] = search_form
        return context


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5
    queryset = Worker.objects.select_related("position")
    template_name = "task_manager/worker/worker_list.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get(key="username", default="")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Worker.objects.select_related("position")
        username = self.request.GET.get("username", "")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "task_manager/worker/worker_detail.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        worker = self.get_object()
        tasks = Task.objects.filter(assignees=worker)
        context["tasks"] = tasks
        return context


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
    success_url = reverse_lazy("task_manager:worker_list")


class WorkerTaskDeleteView(LoginRequiredMixin, ModelDeleteMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        worker_id = kwargs.get("worker_pk")
        task_id = kwargs.get("task_pk")
        self.remove_object(task_id, worker_id, "assignees", Task, Worker)
        return HttpResponseRedirect(reverse_lazy("task_manager:worker_detail", args=[worker_id]))


class WorkerTaskAddView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerTaskAddForm
    template_name = "task_manager/worker/worker_form.html"

    def form_valid(self, form):
        worker = form.save(commit=False)
        tasks = form.cleaned_data['tasks']
        for task in tasks:
            task.assignees.add(worker)
            task.save()
        return HttpResponseRedirect(self.get_success_url())


class TaskListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Task
    paginate_by = 3
    template_name = "task_manager/task/task_list.html"
    search_form_class = TaskSearchForm
    search_fields = ["name"]
    queryset = (
        Task.objects
        .select_related("task_type")
        .prefetch_related("assignees", "teams", "tags")
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


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/task/task_delete.html"
    success_url = reverse_lazy("task_manager:task_list")


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
        if request.GET.get('next'):
            cache.clear()
            return HttpResponseRedirect(request.GET['next'])
        else:
            return HttpResponseRedirect(reverse_lazy("task_manager:task_detail", args=[task_id]))


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


class TeamListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Team
    queryset = Team.objects.all().prefetch_related("member", "task", "projects")
    template_name = "task_manager/team/team_list.html"
    search_form_class = TeamSearchForm
    search_fields = ["name"]


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
    success_url = reverse_lazy("task_manager:team_list")
    template_name = "task_manager/team/team_delete.html"


class TeamTaskDeleteView(LoginRequiredMixin, ModelDeleteMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get("team_pk")
        self.remove_object(team_id, kwargs.get("task_pk"), "task", Team, Task)
        return HttpResponseRedirect(reverse_lazy("task_manager:team_list"))


class TeamMemberDeleteView(LoginRequiredMixin, ModelDeleteMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get("team_pk")
        self.remove_object(team_id, kwargs.get("member_pk"), "member", Team, Worker)
        return HttpResponseRedirect(reverse_lazy("task_manager:team_list"))


class TeamTaskAddView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamTaskAddForm
    template_name = "task_manager/team/team_form.html"


class TeamMemberAddView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamMemberAddForm
    template_name = "task_manager/team/team_form.html"


class TagListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Tag
    paginate_by = 4
    queryset = Tag.objects.prefetch_related("tasks")
    template_name = "task_manager/tag/tag_list.html"
    search_form_class = TagSearchForm
    search_fields = ["name"]


class TagFormMixin(LoginRequiredMixin, generic.UpdateView):
    template_name = "task_manager/tag/tag_form.html"
    success_url = reverse_lazy("task_manager:tag_list")

    def get(self, request, *args, **kwargs):
        instance = None
        if "pk" in kwargs:
            instance = get_object_or_404(Tag, pk=kwargs["pk"])
        form = TagCreateForm(instance=instance)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        instance = None
        if "pk" in kwargs:
            instance = get_object_or_404(Tag, pk=kwargs["pk"])
        form = TagCreateForm(request.POST, instance=instance)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            tasks = form.cleaned_data.get("tasks", [])
            tag.tasks.set(tasks)
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})


class TagCreateView(TagFormMixin, generic.CreateView):
    pass


class TagUpdateView(TagFormMixin, generic.UpdateView):
    pass


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    template_name = "task_manager/tag/tag_delete.html"
    success_url = reverse_lazy("task_manager:tag_list")


class ProjectListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Project
    paginate_by = 3
    queryset = Project.objects.select_related("team").prefetch_related("task")
    template_name = "task_manager/project/project_list.html"
    search_form_class = ProjectSearchForm
    search_fields = ["name"]


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "task_manager/project/project_form.html"
    success_url = reverse_lazy("task_manager:project_list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "task_manager/project/project_form.html"


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    template_name = "task_manager/project/project_delete.html"
    success_url = reverse_lazy("task_manager:project_list")


class ProjectTaskDeleteView(LoginRequiredMixin, ModelDeleteMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        project_id = kwargs.get("project_pk")
        self.remove_object(project_id, kwargs.get("task_pk"), "task", Project, Task)
        return HttpResponseRedirect(self.get_success_url())


class ProjectTeamDeleteView(LoginRequiredMixin, ModelDeleteMixin, generic.UpdateView):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get("project_pk"))
        project.team = None
        project.save()
        return HttpResponseRedirect(self.get_success_url())
