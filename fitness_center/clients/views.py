from django.views.generic import ListView, View, TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ApplicationForm
from trainers.models import TrainerProfile, TrainingApplication
from clients.models import ClientProfile
from workouts.models import TrainingPlan, PlanExercise, DailyExerciseLog
from workouts.forms import DailyLogFormSet
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from trainers.models import TrainingApplication
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

from workouts.models import DailyExerciseLog, PlanExercise

class MyPlanView(LoginRequiredMixin, View):
    template_name = 'clients/my_plan.html'

    def get(self, request):
        logs = DailyExerciseLog.objects.filter(
            client=request.user.clientprofile,
            date=date.today()
        ).select_related('exercise')
        return render(request, self.template_name, {
            'logs': logs
        })

class SaveProgressView(LoginRequiredMixin, View):
    def post(self, request):
        logs = DailyExerciseLog.objects.filter(
            client=request.user.clientprofile,
            date=date.today()
        )
        for log in logs:
            completed = request.POST.get(f'completed_{log.id}') == 'on'
            heart_rate = request.POST.get(f'heart_rate_{log.id}')
            log.completed = completed
            log.heart_rate = heart_rate if heart_rate else None
            log.save()
        return redirect('clients:my_plan')

@login_required
def my_applications(request):
    applications = TrainingApplication.objects.filter(client=request.user.clientprofile).order_by('-created_at')
    return render(request, 'clients/my_applications.html', {
        'applications': applications
    })
class TrainerListView(LoginRequiredMixin, ListView):
    model = TrainerProfile
    template_name = 'clients/trainer_list.html'
    context_object_name = 'trainers'

class ApplicationCreateView(LoginRequiredMixin, View):
    template_name = 'clients/trainer_apply.html'

    def get(self, request, pk):
        trainer = get_object_or_404(TrainerProfile, pk=pk)
        form = ApplicationForm()
        return render(request, self.template_name, {'trainer': trainer, 'form': form})

    def post(self, request, pk):
        trainer = get_object_or_404(TrainerProfile, pk=pk)
        client = get_object_or_404(ClientProfile, user=request.user)
        form = ApplicationForm(request.POST)
        if form.is_valid():
            TrainingApplication.objects.create(
                client=client,
                trainer=trainer,
                goal=form.cleaned_data['goal']
            )
            return redirect('clients:application_list')
        return render(request, self.template_name, {'trainer': trainer, 'form': form})

class ApplicationListView(LoginRequiredMixin, ListView):
    template_name = 'clients/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        client = get_object_or_404(ClientProfile, user=self.request.user)
        return TrainingApplication.objects.filter(client=client).order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        # добавляем атрибут days_waiting каждому объекту
        for app in ctx['applications']:
            delta = today - app.created_at.date()
            app.days_waiting = delta.days
        return ctx

class PlanDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'clients/my_plan.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        client = get_object_or_404(ClientProfile, user=self.request.user)
        plan = TrainingPlan.objects.filter(client=client).order_by('-start_date').first()
        ctx['plan'] = plan
        ctx['exercises'] = plan.plan_exercises.select_related('exercise') if plan else []
        return ctx
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from clients.models import ClientProfile
from workouts.models import TrainingPlan, DailyExerciseLog, PlanExercise
from datetime import date

class PlanTabView(LoginRequiredMixin, View):
    template_name = 'clients/plan_tabs.html'

    def get(self, request):
        context = self._build_context(request)
        return render(request, self.template_name, context)

    def post(self, request):
        client = get_object_or_404(ClientProfile, user=request.user)
        today = date.today()

        # получаем записи лога на сегодня
        logs = DailyExerciseLog.objects.filter(client=client, date=today)
        # сохраняем каждую запись
        for log in logs:
            log.completed = f'completed_{log.id}' in request.POST
            hr = request.POST.get(f'heart_rate_{log.id}')
            if hr:
                try:
                    log.heart_rate = int(hr)
                except ValueError:
                    pass
            log.save()

        return redirect('clients:plan_tabs')

    def _build_context(self, request):
        client = get_object_or_404(ClientProfile, user=request.user)
        today = date.today()

        plan = TrainingPlan.objects.filter(client=client, start_date__lte=today).order_by('-start_date').first()
        full_plan = []
        logs = []
        if plan:
            # получаем упражнения плана
            pes = PlanExercise.objects.filter(plan=plan).select_related('exercise')
            # готовим список для отображения полного плана
            for pe in pes:
                full_plan.append({
                    'exercise': pe.exercise.name,
                    'frequency': pe.frequency_per_week,
                    'sets': pe.sets,
                    'reps': pe.reps,
                })
                # обеспечиваем запись лога
                log, _ = DailyExerciseLog.objects.get_or_create(
                    client=client, date=today, exercise=pe.exercise,
                    defaults={'completed': False, 'heart_rate': None}
                )
                logs.append({
                    'id': log.id,
                    'exercise': pe.exercise.name,
                    'frequency': pe.frequency_per_week,
                    'sets': pe.sets,
                    'reps': pe.reps,
                    'completed': log.completed,
                    'heart_rate': log.heart_rate,
                })

        total = len(logs)
        done = sum(1 for l in logs if l['completed'])
        today_percent = int(done / total * 100) if total else 0
        remaining_percent = 100 - today_percent

        return {
            'plan_exists': bool(plan),
            'full_plan': full_plan,
            'logs': logs,
            'today': today,
            'today_percent': today_percent,
            'remaining_percent': remaining_percent,
        }


class TodayExercisesView(LoginRequiredMixin, View):
    template_name = 'clients/today_exercises.html'

    def get(self, request):
        client = get_object_or_404(ClientProfile, user=request.user)
        today = date.today()
        plan = TrainingPlan.objects.filter(client=client, start_date__lte=today).order_by('-start_date').first()
        if not plan:
            return render(request, self.template_name, {'no_plan': True, 'today': today})
        # prepare logs
        logs = []
        for pe in plan.plan_exercises.select_related('exercise'):
            log, _ = DailyExerciseLog.objects.get_or_create(
                client=client, date=today, exercise=pe.exercise,
                defaults={'completed': False, 'heart_rate': None}
            )
            logs.append(log)
        formset = DailyLogFormSet(queryset=DailyExerciseLog.objects.filter(id__in=[l.id for l in logs]))
        return render(request, self.template_name, {'formset': formset, 'today': today})

    def post(self, request):
        client = get_object_or_404(ClientProfile, user=request.user)
        today = date.today()
        qs = DailyExerciseLog.objects.filter(client=client, date=today)
        formset = DailyLogFormSet(request.POST, queryset=qs)
        if formset.is_valid():
            formset.save()
            return redirect('clients:today_exercises')
        return render(request, self.template_name, {'formset': formset, 'today': today})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from clients.forms import TrainerChangeForm
from trainers.models import TrainingApplication

@login_required
def change_trainer(request):
    if request.user.role != 'client':
        return redirect('accounts:profile')

    existing_pending = TrainingApplication.objects.filter(
        client=request.user.clientprofile,
        status='pending'
    ).exists()

    if existing_pending:
        return render(request, 'clients/change_trainer.html', {
            'form': None,
            'error': 'У вас уже есть неподтверждённая заявка.'
        })

    if request.method == 'POST':
        form = TrainerChangeForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.client = request.user.clientprofile
            app.save()
            return redirect('clients:applications')
    else:
        form = TrainerChangeForm()

    return render(request, 'clients/change_trainer.html', {'form': form})
