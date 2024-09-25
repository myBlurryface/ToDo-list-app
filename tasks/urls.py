from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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

    # Установка статуса задачи complete
    path('tasks/<int:pk>/complete/', views.MarkTaskCompletedView.as_view(), name='task-complete'),

    # Фильтр задач по статусу
    path('tasks/status/<str:status>/', views.TaskFilterStatusView.as_view(), name='task-filter-by-status'),

    # JWT - эндпоинты
    # Получение refresh и acess токенов
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),  
    # Обновление acess токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'), 
]


