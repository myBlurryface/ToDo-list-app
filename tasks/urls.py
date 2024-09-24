from django.urls import path
from . import views      

urlpatterns = [
    # Получение списка всех задач
    path('tasks/', views.TaskListView.as_view(), name='task-list'),

    # Получение списка задач пользователя по 'username'
    path('tasks/user/<str:username>/', views.UserTasksView.as_view(), name='user-task-list'),

    # Получение инфо о задаче по UID
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),

    # Создание новой задачи
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),

    # Обновление задачи по UID (только владельцем)
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),

    # Удаление задачи по UID (только владельцем)
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
]


