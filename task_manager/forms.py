from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Message, Worker, Task, Team, Tag, Project


class StyleFormMixin(forms.ModelForm):
    class Meta:
        attrs = {
            "style": "background-color:rgba(220, 240, 220, 0.5); margin-bottom: 20px",

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ != forms.CheckboxSelectMultiple:
                field.widget.attrs.update(self.Meta.attrs)


class MessageForm(StyleFormMixin, forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={
            "placeholder": "  Enter your message..."
        }), label="")

    class Meta:
        model = Message
        fields = ["text"]
        attrs = StyleFormMixin.Meta.attrs


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
            "tags": forms.CheckboxSelectMultiple()
        }
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


class ProjectForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "task": forms.CheckboxSelectMultiple(),
        }
        attrs = StyleFormMixin.Meta.attrs


class SearchFormMixin(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Enter name..."}),
        required=False,
        label=""
    )

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(SearchFormMixin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "common-form-field-style"})


class TaskSearchForm(SearchFormMixin, StyleFormMixin):
    class Meta:
        model = Task
        fields = ["name"]
        attrs = StyleFormMixin.Meta.attrs


class TeamSearchForm(SearchFormMixin, StyleFormMixin):
    class Meta:
        model = Team
        fields = ["name"]
        attrs = StyleFormMixin.Meta.attrs


class TagSearchForm(SearchFormMixin, StyleFormMixin):
    class Meta:
        model = Tag
        fields = ["name"]
        attrs = StyleFormMixin.Meta.attrs


class ProjectSearchForm(SearchFormMixin, StyleFormMixin):
    class Meta:
        model = Project
        fields = ["name"]
        attrs = StyleFormMixin.Meta.attrs


class WorkerSearchForm(StyleFormMixin, forms.ModelForm):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Enter username..."}),
        required=False,
        label=""
    )

    class Meta:
        model = Worker
        fields = ["username"]
        attrs = StyleFormMixin.Meta.attrs
