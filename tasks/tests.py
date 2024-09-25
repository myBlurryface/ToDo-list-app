from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Task
import json

User = get_user_model()

class TaskAPITestCase(APITestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.user1 = User.objects.create_user(
            username='testuser1', password='testpass1', first_name='Test1', last_name='User1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', password='testpass2', first_name='Test2', last_name='User2'
        )

        # Получаем токен для user1
        response = self.client.post(reverse('token-obtain-pair'), {
            'username': 'testuser1',
            'password': 'testpass1'
        })
        self.token = response.data['access']

        # Устанавливаем заголовки авторизации 
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Создаем несколько тестовых задач 
        self.task1 = Task.objects.create(
            title="Test Task 1", description="Description 1", status="new", user=self.user1
        )
        self.task2 = Task.objects.create(
            title="Test Task 2", description="Description 2", status="in_progress", user=self.user1
        )
        self.task3 = Task.objects.create(
            title="Test Task 3", description="Description 3", status="completed", user=self.user2
        )

    def test_create_task(self):
        """ Создание задачи """
        data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'status': 'new'
        }
        response = self.client.post(reverse('task-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)

    def test_get_task_list(self):
        """ Получение списка задач """
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 3)   

    def test_get_task_by_username(self):
        """ Получение задач по имени пользователя """
        response = self.client.get(reverse('user-task-list', args=['testuser1']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)   

        response = self.client.get(reverse('user-task-list', args=['testuser2']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)   

    def test_mark_task_completed(self):
        """ Отметить задачу как выполнена """
        response = self.client.put(reverse('task-complete', args=[self.task1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, 'completed')   

    def test_filter_tasks_by_status(self):
        """ Фильтрация задач по статусу """
        response = self.client.get(reverse('task-filter-by-status', args=['new']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)   

        response = self.client.get(reverse('task-filter-by-status', args=['in_progress']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)   

        response = self.client.get(reverse('task-filter-by-status', args=['completed']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)   

    def test_update_task(self):
        """ Обновление задачи владельцем """
        data = {'title': 'Updated Task Title', 'description': 'Updated Description', 'status': 'in_progress'}
        response = self.client.put(reverse('task-update', args=[self.task1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task Title')

    def test_update_task_not_owner(self):
        """ Задачу обновляет только владелец """
        self.client.logout()   
        # Логирумся как второй пользователь
        response = self.client.post(reverse('token-obtain-pair'), {
            'username': 'testuser2',
            'password': 'testpass2'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        data = {'title': 'Unauthorized Update', 'description': 'Attempt to update', 'status': 'new'}
        response = self.client.put(reverse('task-update', args=[self.task1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        """ Удаление задачи """
        response = self.client.delete(reverse('task-delete', args=[self.task1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.filter(id=self.task1.id).count(), 0)   

    def test_delete_task_not_owner(self):
        """ Задачу может удалять только владелец """
        self.client.logout()  
        
        response = self.client.post(reverse('token-obtain-pair'), {
            'username': 'testuser2',
            'password': 'testpass2'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.delete(reverse('task-delete', args=[self.task1.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.filter(id=self.task1.id).count(), 1)  
    
    def test_pagination(self):
        """ Пагинация """
        # Создаем дополнительные задачи для проверки пагинации
        for i in range(10):
            Task.objects.create(title=f"Task {i+4}", description="Bulk task", status="new", user=self.user1)

        response = self.client.get(reverse('task-list'), {'page': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('next' in response.data or 'previous' in response.data)  

    def test_authentication_required(self):
        """ Доступ только авторизованным пользователям """
        self.client.logout()  

        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   
