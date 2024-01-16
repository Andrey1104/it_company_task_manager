from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Message, Worker, Task


class MessageForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={
            "placeholder": "  Enter your message..."
        }), label="")

    class Meta:
        model = Message
        fields = ["text"]


class WorkerCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
        )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = (
            "first_name",
            "last_name",
            "email",
            "position",
        )


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "assignees": forms.CheckboxSelectMultiple()
        }


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "assignees": forms.CheckboxSelectMultiple(),
            "tags": forms.CheckboxSelectMultiple()
        }