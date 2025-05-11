from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('plan/', views.PlanDetailView.as_view(), name='my_plan'),
    path('today/', views.TodayExercisesView.as_view(), name='today_exercises'),
]
