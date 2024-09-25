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
    queryset = Task.objects.all()
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

    # Блокируем удаление
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Deletion via this endpoint is not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Блокируем обновление (PUT)
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Update via this endpoint is not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Блокируем частичное обновление (PATCH)
    def patch(self, request, *args, **kwargs):
        return Response({"detail": "Partial update via this endpoint is not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_object(self):
        task = super().get_object()
        return task


# Создание новой задачи текущему пользователю
class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer  
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  


# Обновление задачи
class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        task = self.get_object()  # Получаем задачу

        # Проверка, является ли пользователь владельцем задачи
        if task.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this task.")

        # Если пользователь является владельцем, сохраняем изменения
        serializer.save()


# Удаление задачи по UID
class TaskDeleteView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        
        if task.user != request.user:
            raise PermissionDenied("You do not have permission to delete this task.")

        task.delete()
        
        return Response({"detail": "Task successfully deleted."}, status=status.HTTP_200_OK)


# Установка статуса 'complete'
class MarkTaskCompletedView(generics.UpdateAPIView):
    serializer_class = TaskSerializer  
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        
        task.status = "completed"
        task.save()

        return Response({"detail": "Task status updated to 'completed'."}, status=status.HTTP_200_OK)


# Фильтрация задач по статусу
class TaskFilterStatusView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status = self.kwargs.get('status') # Получение статуса из запроса
        return Task.objects.filter(status=status)
