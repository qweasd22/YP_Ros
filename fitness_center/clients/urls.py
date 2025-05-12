from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('trainers/', views.TrainerListView.as_view(), name='trainer_list'),
    path('trainers/<int:pk>/apply/', views.ApplicationCreateView.as_view(), name='trainer_apply'),
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('plan/', views.PlanTabView.as_view(), name='plan_tabs'),
    path('change_trainer/', views.change_trainer, name='change_trainer'),
    path('my_applications/', views.my_applications, name='my_applications'),
    
]
