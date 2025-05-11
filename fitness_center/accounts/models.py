from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group, Permission
from .managers import UserManager
class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('trainer', 'Тренер'),
        ('admin', 'Администратор'),
    )
    username = None  

    # Новые поля
    phone = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('M','Муж.'),('F','Жен.')))
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    # Переопределяем поля групп и прав, чтобы не было конфликтов:
    groups = models.ManyToManyField(
        Group,
        related_name="accounts_user_set",
        blank=True,
        help_text="Группы, к которым принадлежит пользователь",
        verbose_name="Группы"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="accounts_user_set_permissions",
        blank=True,
        help_text="Дополнительные права конкретного пользователя",
        verbose_name="Права пользователя"
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()  # <-- здесь
    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"
