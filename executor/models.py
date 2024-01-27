from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from it_company_task_manager import settings

from task.models import Task


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
        null=True,
    )

    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self) -> str:
        return reverse("executor:worker_detail", args=[str(self.id)])


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
        return reverse("executor:team_list")


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="projects",
        blank=True,
        null=True,
    )
    task = models.ManyToManyField(Task, related_name="projects", blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_absolute_url() -> str:
        return reverse("executor:project_list")
