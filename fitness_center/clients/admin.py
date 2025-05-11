from django.contrib import admin
from .models import ClientProfile
from django.contrib import admin
from accounts.models import User
from accounts.admin import UserAdmin
@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'trainer', 'discount')
    list_filter = ('trainer',)
    search_fields = ('user__full_name', 'user__phone')
    raw_id_fields = ('user', 'trainer')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # если это новый клиент и у него нет профиля — создаём
        if not change and obj.role == 'client':
            ClientProfile.objects.get_or_create(user=obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)