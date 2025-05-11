from django.contrib import admin
from .models import TrainerProfile, TrainingApplication

class ApplicationInline(admin.TabularInline):
    model = TrainingApplication
    fields = ('client', 'goal', 'status', 'created_at', 'responded_at')
    readonly_fields = ('created_at', 'responded_at')
    extra = 0

@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience_years')
    list_filter = ('experience_years',)
    search_fields = ('user__full_name',)
    inlines = (ApplicationInline,)
    raw_id_fields = ('user',)

@admin.register(TrainingApplication)
class TrainingApplicationAdmin(admin.ModelAdmin):
    list_display = ('client', 'trainer', 'status', 'created_at', 'responded_at')
    list_filter = ('status', 'trainer')
    search_fields = ('client__user__full_name', 'trainer__user__full_name')
    readonly_fields = ('created_at', 'responded_at')
    actions = ['make_accepted', 'make_rejected']

    def make_accepted(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='accepted', responded_at=admin.utils.timezone.now())
        self.message_user(request, f"{updated} заявка(ок) отмечено как «Принята».")
    make_accepted.short_description = "Отметить выбранные заявки как принятые"

    def make_rejected(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected', responded_at=admin.utils.timezone.now())
        self.message_user(request, f"{updated} заявка(ок) отмечено как «Отклонена».")
    make_rejected.short_description = "Отметить выбранные заявки как отклонённые"
