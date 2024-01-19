from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from task_manager.models import TaskType, Position, Worker, Tag, Task, Message, Team, Project


class TaskManagerViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.task_type = TaskType.objects.create(name="Type")
        self.position = Position.objects.create(name="Position")
        self.user = get_user_model().objects.create_user(
            username='testuser123',
            password='testpassword12'
        )
        self.worker = Worker.objects.create(
            username='worker123',
            password='password123',
            first_name='John',
            last_name='Doe',
            position=self.position
        )
        self.tag = Tag.objects.create(name="Tag")

        self.task = Task.objects.create(
            name='Task',
            description='description',
            deadline=timezone.now(),
            is_completed=False,
            priority='HIGH',
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)
        self.task.tags.add(self.tag)
        self.message = Message.objects.create(
            author=self.user,
            text='Sample message',
            task=self.task,
        )
        self.team = Team.objects.create(name="Sample Team")
        self.team.member.add(self.user)
        self.project = Project.objects.create(
            name="Sample Project",
            description="Project description",
            deadline=timezone.now(),
            team=self.team
        )
        self.client.force_login(self.worker)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'layouts/index.html')

    def test_message_create_view(self):
        response = self.client.post(reverse('task_manager:message_create', kwargs={'pk_author': self.worker.pk, 'pk_task': self.task.pk}), data={'text': 'New message'})
        self.assertEqual(response.status_code, 302)

    def test_message_delete_view(self):
        response = self.client.get(reverse('task_manager:message_delete', kwargs={'task_pk': self.task.pk, 'message_pk': self.message.pk}))
        self.assertEqual(response.status_code, 302)

    def test_chat_create_view(self):
        response = self.client.post(reverse('task_manager:chat_create'), data={'task': self.task.pk})
        self.assertEqual(response.status_code, 302)

    def test_project_update_view(self):
        response = self.client.get(reverse('task_manager:project_update', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/project/project_form.html')
        updated_data = {
            'name': 'Updated Project Name',
        }
        response = self.client.post(reverse(
            'task_manager:project_update',
            args=[self.project.pk]),
            data=updated_data)
        self.assertEqual(response.status_code, 200)

    def test_project_delete_view(self):
        response = self.client.get(reverse('task_manager:project_delete', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/project/project_delete.html')

        response = self.client.post(reverse('task_manager:project_delete', args=[self.project.pk]))
        self.assertEqual(response.status_code, 302)

    def test_project_task_delete_view(self):
        response = self.client.get(
            reverse('task_manager:project_task_delete', args=[self.project.pk, self.task.pk]))
        self.assertEqual(response.status_code, 302)

    def test_tag_list_view(self):
        response = self.client.get(reverse('task_manager:tag_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/tag/tag_list.html')

    def test_tag_create_view(self):
        response = self.client.get(reverse('task_manager:tag_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/tag/tag_form.html')

    def test_tag_update_view(self):
        response = self.client.get(reverse('task_manager:tag_update', args=[self.tag.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/tag/tag_form.html')
        updated_data = {
            'name': 'Updated Tag Name',
        }
        response = self.client.post(reverse(
            'task_manager:tag_update',
            args=[self.tag.pk]),
            data=updated_data)
        self.assertEqual(response.status_code, 302)

    def test_tag_delete_view(self):
        response = self.client.get(reverse(
            'task_manager:tag_delete',
            args=[self.tag.pk]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/tag/tag_delete.html')

        response = self.client.post(reverse('task_manager:tag_delete', args=[self.tag.pk]))
        self.assertEqual(response.status_code, 302)

    def test_task_list_view(self):
        response = self.client.get(reverse('task_manager:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task/task_list.html')

    def test_task_detail_view(self):
        response = self.client.get(reverse('task_manager:task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task/task_detail.html')

    def test_task_create_view(self):
        response = self.client.get(reverse('task_manager:task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task/task_form.html')
        task_data = {
            'name': 'Test Task',
        }
        response = self.client.post(reverse('task_manager:task_create'), data=task_data)
        self.assertEqual(response.status_code, 200)

    def test_task_update_view(self):
        response = self.client.get(reverse('task_manager:task_update', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task/task_form.html')
        updated_data = {
            'name': 'Updated Task Name',
        }
        response = self.client.post(reverse(
            'task_manager:task_update',
            args=[self.task.pk]),
            data=updated_data)
        self.assertEqual(response.status_code, 200)

    def test_task_delete_view(self):
        response = self.client.get(reverse('task_manager:task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task/task_delete.html')

        response = self.client.post(reverse('task_manager:task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)

    def test_task_status_update_view(self):
        response = self.client.get(reverse('task_manager:task_status_update', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)

    def test_team_list_view(self):
        response = self.client.get(reverse('task_manager:team_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/team/team_list.html')

    def test_team_create_view(self):
        response = self.client.get(reverse('task_manager:team_create'))
        self.assertEqual(response.status_code, 200)
        team_data = {
            'name': 'Test Team',
        }
        response = self.client.post(reverse('task_manager:team_create'), data=team_data)
        self.assertEqual(response.status_code, 200)

    def test_team_update_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task_manager:team_update', args=[self.team.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/team/team_form.html')
        updated_data = {
            'name': 'Updated Team Name',
        }
        response = self.client.post(reverse('task_manager:team_update', args=[self.team.pk]), data=updated_data)
        self.assertEqual(response.status_code, 200)

    def test_team_delete_view(self):
        response = self.client.get(reverse('task_manager:team_delete', args=[self.team.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/team/team_delete.html')

        response = self.client.post(reverse('task_manager:team_delete', args=[self.team.pk]))
        self.assertEqual(response.status_code, 302)

    def test_team_task_delete_view(self):
        response = self.client.get(reverse('task_manager:team_task_delete', args=[self.team.pk, self.task.pk]))
        self.assertEqual(response.status_code, 302)

    def test_team_member_delete_view(self):
        response = self.client.get(reverse('task_manager:team_member_delete', args=[self.team.pk, self.worker.pk]))
        self.assertEqual(response.status_code, 302)

    def test_team_task_add_view(self):
        response = self.client.get(reverse('task_manager:team_task_add', args=[self.team.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/team/team_form.html')
        task_data = {
            'task': self.task.pk,
        }
        response = self.client.post(reverse('task_manager:team_task_add', args=[self.team.pk]), data=task_data)
        self.assertEqual(response.status_code, 302)

    def test_team_member_add_view(self):
        response = self.client.get(reverse('task_manager:team_member_add', args=[self.team.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/team/team_form.html')
        member_data = {
            'member': self.worker.pk,
        }
        response = self.client.post(reverse('task_manager:team_member_add', args=[self.team.pk]), data=member_data)
        self.assertEqual(response.status_code, 302)

    def test_worker_list_view(self):
        response = self.client.get(reverse('task_manager:worker_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/worker/worker_list.html')

    def test_worker_detail_view(self):
        response = self.client.get(reverse('task_manager:worker_detail', args=[self.worker.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/worker/worker_detail.html')

    def test_worker_create_view(self):
        response = self.client.get(reverse('task_manager:worker_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/worker/worker_form.html')
        worker_data = {
            'username': 'TestWorker',
        }
        response = self.client.post(reverse('task_manager:worker_create'), data=worker_data)
        self.assertEqual(response.status_code, 200)

    def test_worker_update_view(self):
        response = self.client.get(reverse('task_manager:worker_update', args=[self.worker.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/worker/worker_form.html')
        updated_data = {
            'username': 'UpdatedWorker',
        }
        response = self.client.post(reverse('task_manager:worker_update', args=[self.worker.pk]), data=updated_data)
        self.assertEqual(response.status_code, 302)

    def test_worker_delete_view(self):
        response = self.client.get(reverse('task_manager:worker_delete', args=[self.worker.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/worker/worker_delete.html')

        response = self.client.post(reverse('task_manager:worker_delete', args=[self.worker.pk]))
        self.assertEqual(response.status_code, 302)

    def test_worker_task_delete_view(self):
        response = self.client.get(reverse('task_manager:worker_task_delete', args=[self.worker.pk, self.task.pk]))
        self.assertEqual(response.status_code, 302)

    def test_worker_task_add_view(self):
        response = self.client.get(reverse('task_manager:worker_task_add', args=[self.worker.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/worker/worker_form.html')
        task_data = {
            'tasks': [self.task.pk],
        }
        response = self.client.post(reverse('task_manager:worker_task_add', args=[self.worker.pk]), data=task_data)
        self.assertEqual(response.status_code, 302)
