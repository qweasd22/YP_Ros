from django.views import View
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from trainers.models import TrainingApplication
from workouts.models import TrainingPlan
from clients.models import ClientProfile
from .forms import TrainingPlanForm, PlanExerciseFormSet
from django.utils import timezone



class AcceptApplicationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        app = get_object_or_404(TrainingApplication, pk=pk, trainer__user=request.user, status='pending')
        app.status = 'accepted'
        app.responded_at = timezone.now()
        app.save()
        client_profile = app.client
        client_profile.trainer = app.trainer
        client_profile.save()
        return redirect('trainers:dashboard')

from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from clients.models import ClientProfile
from workouts.models import TrainingPlan
from .models import TrainingApplication
from .forms import TrainingPlanForm, PlanExerciseFormSet
from django.utils import timezone

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'trainers/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        trainer = self.request.user.trainerprofile
        # все клиенты, у которых есть принятая заявка к этому тренеру
        accepted_apps = TrainingApplication.objects.filter(
            trainer=trainer, status='accepted'
        )
        ctx['clients_with_apps'] = [app.client for app in accepted_apps]
        # заявки в ожидании
        ctx['pending_apps'] = TrainingApplication.objects.filter(
            trainer=trainer, status='pending'
        )
        return ctx

class PlanCreateView(LoginRequiredMixin, View):
    template_name = 'trainers/plan_create.html'

    def get(self, request, pk):
        client = get_object_or_404(ClientProfile, pk=pk, trainer__user=request.user)
        plan_form = TrainingPlanForm()
        formset = PlanExerciseFormSet()
        return render(request, self.template_name, {
            'client': client,
            'plan_form': plan_form,
            'formset': formset
        })

    def post(self, request, pk):
        client = get_object_or_404(ClientProfile, pk=pk, trainer__user=request.user)
        plan_form = TrainingPlanForm(request.POST)
        formset = PlanExerciseFormSet(request.POST)
        if plan_form.is_valid() and formset.is_valid():
            # проверяем, что есть хотя бы один заполненный подформ
            has_data = any(
                f.cleaned_data and not f.cleaned_data.get('DELETE', False)
                for f in formset.forms
            )
            if not has_data:
                formset.non_form_errors = ['Нужно добавить хотя бы одно упражнение.']
            else:
                # сохраняем план
                plan = plan_form.save(commit=False)
                plan.client = client
                plan.save()
                formset.instance = plan
                formset.save()
                # после сохранения возвращаем на дашборд
                return redirect('trainers:dashboard')
        # при ошибках валидации или отсутствии строк показываем форму снова
        return render(request, self.template_name, {
            'client': client,
            'plan_form': plan_form,
            'formset': formset
        })
    def _generate_logs(self, plan):
        exercises = plan.plan_exercises.all()
        current_date = plan.start_date
        days_count = 30  # План на 30 дней вперёд

        for day_offset in range(days_count):
            day = current_date + timedelta(days=day_offset)
            for ex in exercises:
                DailyExerciseLog.objects.get_or_create(
                    client=plan.client,
                    date=day,
                    exercise=ex.exercise,
                )


from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import TrainingApplication
from workouts.models import DailyExerciseLog
from datetime import timedelta

def generate_logs_for_plan(plan):
    exercises = plan.plan_exercises.all()
    current_date = plan.start_date
    days_count = 30  # Пример: генерим на 30 дней вперёд

    for day_offset in range(days_count):
        day = current_date + timedelta(days=day_offset)
        for ex in exercises:
            # Лог создаём только если его ещё нет
            DailyExerciseLog.objects.get_or_create(
                client=plan.client,
                date=day,
                exercise=ex.exercise,
            )
@login_required
def accept_application(request, pk):
    app = get_object_or_404(TrainingApplication, pk=pk, trainer__user=request.user)
    app.status = 'accepted'
    app.responded_at = timezone.now()
    app.save()

    # Меняем тренера у клиента
    client = app.client
    client.trainer = app.trainer
    client.save()

    return redirect('trainers:dashboard')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from workouts.models import TrainingPlan, DailyExerciseLog

from django.db.models import Count, Q, Avg
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clients.models import ClientProfile
from workouts.models import DailyExerciseLog

@login_required
def trainer_statistics(request):
    trainer = request.user.trainerprofile

    # Все клиенты этого тренера
    clients = ClientProfile.objects.filter(trainer=trainer)

    stats = []
    for client in clients:
        logs = DailyExerciseLog.objects.filter(client=client)

        total_logs = logs.count()
        completed_logs = logs.filter(completed=True).count()

        percent_completed = (completed_logs / total_logs * 100) if total_logs else 0

        avg_pulse = logs.filter(heart_rate__isnull=False).aggregate(Avg('heart_rate'))['heart_rate__avg'] or 0

        stats.append({
            'client': client,
            'percent_completed': round(percent_completed, 1),
            'avg_pulse': round(avg_pulse, 1),
        })

    return render(request, 'trainers/statistics.html', {
        'stats': stats
    })


