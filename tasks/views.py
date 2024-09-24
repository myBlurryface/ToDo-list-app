from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework import filters
from django.contrib.auth import get_user_model
from .models import Task
from .serializers import TaskSerializer


# Получение списка всех задач
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer 
    permission_classes = [permissions.IsAuthenticated]

# Получение задач пользователя по 'username'
class UserTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        User = get_user_model()
        username = self.kwargs.get('username')

        # Если в запросе передан username, выводим список по этому username
        if username:
            user = User.objects.get(username=username)
            return Task.objects.filter(user=user)

        # Если username не указан, выводим список по username текущего пользователя
        return Task.objects.filter(user=self.request.user)


# Получение задачи по ее UID
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        task = super().get_object()
        return task


# Создание новой задачи текущему пользователю
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()  
    serializer_class = TaskSerializer  
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)    


# Обновление задачи
class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_object(self):
        task = super().get_object()
        if task.user != self.request.user: # Проверяем, является ли обновляющий владельцем задачи
            raise PermissionDenied("Вы не можете редактировать эту задачу, так как не являетесь её владельцем.")
        return task


# Удаление задачи
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_object(self):
        task = super().get_object()
        if task.user != self.request.user: # Проверяем, является ли удаляющий владельцем задачи
            raise PermissionDenied("Вы не можете удалить эту задачу, так как не являетесь её владельцем.")
        return task


# Установка статуса в завершено 'complete'
class MarkTaskCompletedView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        task = self.get_object()
        if task.user != self.request.user: # Изменять статус задачи может только хозяин
            return Response({'detail': 'У вас нет прав на изменение этой задачи.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Изменение статуса задачи
        task.status = 'completed'
        task.save()
        return Response({'detail': 'Задача успешно отмечена как выполненная.'}, status=status.HTTP_200_OK)


# Фильтрация задач по статусу
class TaskFilterStatusView(TaskListView):
    def get_queryset(self):
        queryset = super().get_queryset()    
        status = self.request.query_params.get('status', None)

        if status: # Если в запросе есть статус, фильтруем по нему
            queryset = queryset.filter(status=status)
        return queryset  # Возвращаем весь список или отфильтрованный

