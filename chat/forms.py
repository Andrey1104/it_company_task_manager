from django import forms

from chat.models import Message
from utils.mixins import StyleFormMixin


class MessageForm(StyleFormMixin, forms.ModelForm):
    text = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "  Input your message and press <<< Enter >>>"
            }
        ),
        label="",
    )

    class Meta:
        model = Message
        fields = ["text"]
        attrs = StyleFormMixin.Meta.attrs


class ChatCreateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ["task"]
        attrs = StyleFormMixin.Meta.attrs
