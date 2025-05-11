from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import RegisterForm
from clients.models import ClientProfile
from trainers.models import TrainerProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = RegisterForm
    model = User
    
    list_display = ('full_name', 'phone', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'gender')
    search_fields = ('full_name', 'phone')
    ordering = ('full_name',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Персональные данные', {'fields': ('full_name', 'birth_date', 'gender', 'photo', 'role')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'phone', 'role', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

    def save_model(self, request, obj, form, change):
        is_new = not change
        # 1) Сначала сохраняем User и все related- и M2M-поля
        super().save_model(request, obj, form, change)

        # 2) Только после этого создаём профиль
        if is_new:
            if obj.role == 'client':
                ClientProfile.objects.get_or_create(user=obj)
            elif obj.role == 'trainer':
                TrainerProfile.objects.get_or_create(user=obj)