from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

from chat.models import Message
from executor.models import (
    Position,
    Worker,
    Task,
    Team,
    Project,
)
from task.models import TaskType, Tag


class TaskManagerModelTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Sample Task Type")
        self.position = Position.objects.create(name="Sample Position")
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.worker = Worker.objects.create(
            username="worker",
            password="password123",
            first_name="John",
            last_name="Doe",
            position=self.position,
        )
        self.tag = Tag.objects.create(name="Sample Tag")
        self.task = Task.objects.create(
            name="Sample Task",
            description="Task description",
            deadline=timezone.now(),
            is_completed=False,
            priority="HIGH",
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)
        self.task.tags.add(self.tag)
        self.message = Message.objects.create(
            author=self.user,
            text="Sample message",
            task=self.task,
        )
        self.team = Team.objects.create(name="Sample Team")
        self.team.member.add(self.user)
        self.project = Project.objects.create(
            name="Sample Project",
            description="Project description",
            deadline=timezone.now(),
            team=self.team,
        )

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Sample Task Type")

    def test_position_str(self):
        self.assertEqual(str(self.position), "Sample Position")

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "John Doe")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Sample Tag")

    def test_task_str(self):
        self.assertEqual(str(self.task), "Sample Task")

    def test_message_str(self):
        expected_str = (
            f"{self.user}: \n Sample message \n {self.message.created_at}"
        )
        self.assertEqual(str(self.message), expected_str)

    def test_team_str(self):
        self.assertEqual(str(self.team), "Sample Team")

    def test_project_str(self):
        self.assertEqual(str(self.project), "Sample Project")

    def test_worker_absolute_url(self):
        expected_url = reverse(
            "executor:worker_detail", args=[str(self.worker.id)]
        )
        self.assertEqual(self.worker.get_absolute_url(), expected_url)

    def test_team_absolute_url(self):
        expected_url = reverse("executor:team_list")
        self.assertEqual(self.team.get_absolute_url(), expected_url)

    def test_project_absolute_url(self):
        expected_url = reverse("executor:project_list")
        self.assertEqual(self.project.get_absolute_url(), expected_url)
