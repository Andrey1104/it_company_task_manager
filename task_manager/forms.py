from django import forms

from task_manager.models import Message


class MessageForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={
            "placeholder": "  Enter your message..."
        }), label="")

    class Meta:
        model = Message
        fields = ["text"]
