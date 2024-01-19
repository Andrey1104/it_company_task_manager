from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import (
    WorkerSearchForm,
    WorkerCreateForm,
    WorkerUpdateForm,
    WorkerTaskAddForm,
)
from task_manager.models import Worker, Task
from task_manager.mixins import ModelDeleteMixin


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 4
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


class WorkerCreateView(generic.CreateView):
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


class WorkerTaskDeleteView(
    LoginRequiredMixin, ModelDeleteMixin, generic.UpdateView
):
    def get(self, request, *args, **kwargs):
        worker_id = kwargs.get("worker_pk")
        task_id = kwargs.get("task_pk")
        self.remove_object(task_id, worker_id, "assignees", Task, Worker)
        return HttpResponseRedirect(
            reverse_lazy("task_manager:worker_detail", args=[worker_id])
        )


class WorkerTaskAddView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerTaskAddForm
    template_name = "task_manager/worker/worker_form.html"

    def form_valid(self, form):
        worker = form.save(commit=False)
        tasks = form.cleaned_data["tasks"]
        for task in tasks:
            task.assignees.add(worker)
            task.save()
        return HttpResponseRedirect(self.get_success_url())
