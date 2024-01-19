from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import TagSearchForm, TagCreateForm
from task_manager.models import Tag
from task_manager.mixins import SearchMixin


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
