from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from it_company_task_manager import settings


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self) -> str:
        return reverse("task_manager:worker_detail", args=[str(self.id)])


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("NON_URGENT", "Non-urgent"),
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("URGENT", "Urgent"),
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="HIGH"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="assigned_tasks"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tasks",
        blank=True,
    )

    class Meta:
        ordering = ("deadline",)

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    text = models.TextField()
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.author}: \n {self.text} \n {self.created_at}"


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    task = models.ManyToManyField(
        Task,
        related_name="teams",
    )
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_absolute_url() -> str:
        return reverse("task_manager:team_list")


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="projects",
        blank=True,
        null=True
    )
    task = models.ManyToManyField(
        Task,
        related_name="projects",
        blank=True
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_absolute_url() -> str:
        return reverse("task_manager:project_list")
