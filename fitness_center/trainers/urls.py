from django.urls import path
from . import views

app_name = 'trainers'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/plan/', views.PlanCreateView.as_view(), name='plan_create'),
]
