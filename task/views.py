from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic

from chat.forms import MessageForm
from task.forms import (
    TagSearchForm,
    TagCreateForm,
    TaskSearchForm,
    TaskCreateForm,
    TaskUpdateForm
)
from task.models import Tag, Task
from utils.mixins import SearchMixin


class TagListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Tag
    paginate_by = 4
    queryset = Tag.objects.prefetch_related("tasks")
    template_name = "task_manager/tag/tag_list.html"
    search_form_class = TagSearchForm
    search_fields = ["name"]


class TagFormMixin(LoginRequiredMixin, generic.UpdateView):
    template_name = "task_manager/tag/tag_form.html"
    success_url = reverse_lazy("task:tag_list")

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
    success_url = reverse_lazy("task:tag_list")


class TaskListView(LoginRequiredMixin, SearchMixin, generic.ListView):
    model = Task
    paginate_by = 4
    template_name = "task_manager/task/task_list.html"
    search_form_class = TaskSearchForm
    search_fields = ["name"]
    queryset = Task.objects.select_related("task_type").prefetch_related(
        "assignees", "teams", "tags"
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
    success_url = reverse_lazy("task:task_list")
    template_name = "task_manager/task/task_form.html"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("task:task_list")
    template_name = "task_manager/task/task_form.html"


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/task/task_delete.html"
    success_url = reverse_lazy("task:task_list")


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
        if request.GET.get("next"):
            cache.clear()
            return HttpResponseRedirect(request.GET["next"])
        else:
            return HttpResponseRedirect(
                reverse_lazy("task:task_detail", args=[task_id])
            )
