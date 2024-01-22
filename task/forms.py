from django import forms

from task.models import Task, Tag
from utils.mixins import StyleFormMixin, SearchFormMixin


class TaskCreateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "assignees": forms.CheckboxSelectMultiple(),
        }

        attrs = StyleFormMixin.Meta.attrs


class TaskUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "assignees": forms.CheckboxSelectMultiple(),
            "tags": forms.CheckboxSelectMultiple(),
        }
        attrs = StyleFormMixin.Meta.attrs


class TagCreateForm(StyleFormMixin, forms.ModelForm):
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.prefetch_related("tags"),
        required=False,
    )

    class Meta:
        model = Tag
        fields = ["name", "tasks"]
        attrs = StyleFormMixin.Meta.attrs
        widgets = {"tasks": forms.SelectMultiple()}


class TaskSearchForm(SearchFormMixin, StyleFormMixin):
    class Meta:
        model = Task
        fields = ["name"]
        attrs = StyleFormMixin.Meta.attrs


class TagSearchForm(SearchFormMixin, StyleFormMixin):
    class Meta:
        model = Tag
        fields = ["name"]
        attrs = StyleFormMixin.Meta.attrs
