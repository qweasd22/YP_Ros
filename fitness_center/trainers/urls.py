from django.urls import path
from . import views

app_name = 'trainers'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('applications/<int:pk>/accept/', views.AcceptApplicationView.as_view(), name='accept_application'),
    path('clients/<int:pk>/create_plan/', views.PlanCreateView.as_view(), name='create_plan'),
    path('statistics/', views.trainer_statistics, name='statistics'),
]
