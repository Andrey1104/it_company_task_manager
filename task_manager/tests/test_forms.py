from django.test import TestCase
from django.contrib.auth import get_user_model

from chat.forms import MessageForm, ChatCreateForm
from chat.models import Message
from executor.models import (
    Task,
    Position,
    Worker,
    Team,
    Project,
)
from executor.forms import WorkerCreateForm, TeamCreateForm
from task.forms import TaskCreateForm, TaskSearchForm
from task.models import TaskType, Tag


class TaskManagerFormTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="task")
        self.position = Position.objects.create(name="position")
        self.user = get_user_model().objects.create_user(
            username="testuser1", password="testpassword123"
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
            deadline="2024-11-11",
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
            deadline="2024-11-11",
            team=self.team,
        )

    def test_message_form(self):
        form_data = {"text": "Test message text"}
        form = MessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_create_form(self):
        form_data = {
            "username": "Testuser123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
            "position": self.position,
        }
        form = WorkerCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_create_form(self):
        form_data = {
            "name": "New Task",
            "description": "Task description",
            "deadline": "2024-01-31",
            "is_completed": False,
            "priority": "HIGH",
            "task_type": "1",
            "assignees": [str(self.user.id)],
            "tags": [str(Tag.objects.create(name="Tag 1").id)],
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_team_create_form(self):
        form_data = {
            "name": "New Team",
            "member": [str(self.user.id)],
            "task": [str(self.task.id)],
        }
        form = TeamCreateForm(data=form_data)
        print(form)
        self.assertTrue(form.is_valid())

    def test_task_search_form(self):
        form_data = {"name": "Search Query"}
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_chat_create_form(self):
        form_data = {"task": self.task}
        form = ChatCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
