from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from task_manager.models import Worker, Task, Team, Project, Position


class TestAdmin(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test1")

        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="password12"
        )
        self.client = Client()
        self.client.force_login(self.admin)
        self.worker = get_user_model().objects.create_user(
            username="user",
            password="password123",
            position=self.position
        )
        self.team = Team.objects.create(name="test2")

    def test_position_on_admin_page(self):
        url = reverse("admin:task_manager_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_position_listed_on_detail_admin_page(self):
        url = reverse(
            "admin:task_manager_worker_change",
            args=[self.worker.id]
        )
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_team_search_fields(self):
        url = reverse("admin:task_manager_worker_changelist") + "?q=test_model"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_model")

    def test_list_filter(self):
        response = self.client.get(reverse(
            "admin:task_manager_worker_changelist"),
            {"team__exact": self.team}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "admin:task_manager_worker_changelist") + f"?e={self.team.id}"
        )


