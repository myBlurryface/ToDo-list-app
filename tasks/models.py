from django.db import models
from django.contrib.auth.models import AbstractUser

# Модель пользователей
class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=20, unique=True, blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=True) # Минимальную длину в 6 символов контролируем на этапе валидации  
                                                
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'password']

    def __str__(self):
        return self.username


# Модель задач
class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'NEW'),
        ('in_progress', 'IN_PROGRESS'),
        ('completed', 'COMPLETED'),
    ]

    title = models.CharField(max_length=80, blank=False, null=False)
    description = models.TextField(max_length=140, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title


