from django import forms
from django.contrib.auth.forms import UserCreationForm

from executor.models import Worker, Team, Project
from task.models import Task
from utils.mixins import StyleFormMixin, SearchFormMixin


class WorkerCreateForm(StyleFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
        )
        attrs = StyleFormMixin.Meta.attrs


class WorkerUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Worker
        fields = (
            "first_name",
            "last_name",
            "email",
            "position",
        )
        attrs = StyleFormMixin.Meta.attrs


class WorkerTaskAddForm(StyleFormMixin, forms.ModelForm):
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.prefetch_related("assignees"),
        required=False,
    )

    class Meta:
        model = Worker
        fields = ["tasks"]
        widgets = {"tasks": forms.CheckboxSelectMultiple()}
        attrs = StyleFormMixin.Meta.attrs


class WorkerSearchForm(StyleFormMixin, forms.ModelForm):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Enter username..."}),
        required=False,
        label="",
    )

    class Meta:
        model = Worker
        fields = ["username"]
        attrs = StyleFormMixin.Meta.attrs


class TeamCreateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"
        widgets = {
            "members": forms.CheckboxSelectMultiple(),
            "tasks": forms.CheckboxSelectMultiple(),
        }
        attrs = StyleFormMixin.Meta.attrs


class TeamTaskAddForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Team
        fields = ["task"]
        widgets = {"task": forms.CheckboxSelectMultiple()}
        attrs = StyleFormMixin.Meta.attrs


class TeamMemberAddForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Team
        fields = ["member"]
        widgets = {"member": forms.CheckboxSelectMultiple()}
        attrs = StyleFormMixin.Meta.attrs


class TeamSearchForm(SearchFormMixin, StyleFormMixin):
    class Meta:
        model = Team
        fields = ["name"]
        attrs = StyleFormMixin.Meta.attrs


class ProjectSearchForm(SearchFormMixin, StyleFormMixin):
    class Meta:
        model = Project
        fields = ["name"]
        attrs = StyleFormMixin.Meta.attrs


class ProjectForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "task": forms.CheckboxSelectMultiple(),
        }
        attrs = StyleFormMixin.Meta.attrs
