from django.contrib import admin
from .models import Exercise, TrainingPlan, PlanExercise, DailyExerciseLog

class PlanExerciseInline(admin.TabularInline):
    model = PlanExercise
    extra = 0
    readonly_fields = ()
    autocomplete_fields = ('exercise',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ('client', 'start_date', 'created_at')
    list_filter = ('start_date',)
    search_fields = ('client__user__full_name',)
    inlines = (PlanExerciseInline,)
    readonly_fields = ('created_at',)
    date_hierarchy = 'start_date'

@admin.register(DailyExerciseLog)
class DailyExerciseLogAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'exercise', 'completed', 'heart_rate')
    list_filter = ('date', 'completed')
    search_fields = ('client__user__full_name', 'exercise__name')
    date_hierarchy = 'date'
