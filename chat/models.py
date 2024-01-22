from django.db import models

from it_company_task_manager import settings
from task.models import Task


class Message(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    text = models.TextField()
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="messages"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.author}: \n {self.text} \n {self.created_at}"
