from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import ProjectSearchForm, ProjectForm
from task_manager.models import Project, Task
from task_manager.mixins import SearchMixin, ModelDeleteMixin


class ProjectListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Project
    paginate_by = 4
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


class ProjectTaskDeleteView(
    LoginRequiredMixin, ModelDeleteMixin, generic.UpdateView
):
    def get(self, request, *args, **kwargs):
        project_id = kwargs.get("project_pk")
        self.remove_object(
            project_id, kwargs.get("task_pk"), "task", Project, Task
        )
        return HttpResponseRedirect(self.get_success_url())


class ProjectTeamDeleteView(
    LoginRequiredMixin, ModelDeleteMixin, generic.UpdateView
):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get("project_pk"))
        project.team = None
        project.save()
        return HttpResponseRedirect(self.get_success_url())
