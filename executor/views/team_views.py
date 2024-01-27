from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from executor.forms import (
    TeamSearchForm,
    TeamCreateForm,
    TeamTaskAddForm,
    TeamMemberAddForm,
)
from executor.models import Team, Task, Worker
from utils.mixins import SearchMixin, ModelDeleteMixin


class TeamListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Team
    paginate_by = 4
    queryset = Team.objects.all().prefetch_related(
        "member", "task", "projects"
    )
    template_name = "task_manager/team/team_list.html"
    search_form_class = TeamSearchForm
    search_fields = ["name"]


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamCreateForm
    template_name = "task_manager/task/task_form.html"
    success_url = reverse_lazy("executor:team_list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"
    template_name = "task_manager/team/team_form.html"


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("executor:team_list")
    template_name = "task_manager/team/team_delete.html"


class TeamTaskDeleteView(
    LoginRequiredMixin, ModelDeleteMixin, generic.UpdateView
):
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get("team_pk")
        self.remove_object(team_id, kwargs.get("task_pk"), "task", Team, Task)
        return HttpResponseRedirect(reverse_lazy("executor:team_list"))


class TeamMemberDeleteView(
    LoginRequiredMixin, ModelDeleteMixin, generic.UpdateView
):
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get("team_pk")
        self.remove_object(
            team_id, kwargs.get("member_pk"), "member", Team, Worker
        )
        return HttpResponseRedirect(reverse_lazy("executor:team_list"))


class TeamTaskAddView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamTaskAddForm
    template_name = "task_manager/team/team_form.html"


class TeamMemberAddView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamMemberAddForm
    template_name = "task_manager/team/team_form.html"
