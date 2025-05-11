from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from clients.models import ClientProfile
from .models import TrainingPlan, PlanExercise, DailyExerciseLog
from .forms import DailyLogFormSet
from django.utils import timezone
from datetime import date
from django.shortcuts import get_object_or_404
class PlanDetailView(LoginRequiredMixin, View):
    template_name = 'workouts/my_plan.html'

    def get(self, request):
        # Проверяем, что пользователь — клиент
        if request.user.role != 'client':
            return redirect('home')  # или бросить 403

        client_profile = get_object_or_404(ClientProfile, user=request.user)
        plan = (TrainingPlan.objects
                    .filter(client=client_profile)
                    .order_by('-start_date')
                    .first())
        exercises = plan.plan_exercises.select_related('exercise') if plan else []
        return render(request, self.template_name, {
            'plan': plan,
            'exercises': exercises,
        })


class TodayExercisesView(LoginRequiredMixin, View):
    template_name = 'workouts/today_exercises.html'

    def get(self, request):
        if request.user.role != 'client':
            return redirect('home')

        client_profile = get_object_or_404(ClientProfile, user=request.user)
        today = date.today()
        plan = (TrainingPlan.objects
                    .filter(client=client_profile, start_date__lte=today)
                    .order_by('-start_date')
                    .first())
        if not plan:
            # Можно перенаправить на страницу создания плана или показать сообщение
            return render(request, self.template_name, {
                'no_plan': True,
                'today': today
            })

        plan_exs = plan.plan_exercises.select_related('exercise')
        logs = []
        for pe in plan_exs:
            log, _ = DailyExerciseLog.objects.get_or_create(
                client=client_profile,
                date=today,
                exercise=pe.exercise,
                defaults={'completed': False}
            )
            logs.append(log)

        formset = DailyLogFormSet(queryset=DailyExerciseLog.objects.filter(id__in=[l.id for l in logs]))
        return render(request, self.template_name, {
            'today': today,
            'plan': plan,
            'formset': formset,
        })

    def post(self, request):
        if request.user.role != 'client':
            return redirect('home')

        client_profile = get_object_or_404(ClientProfile, user=request.user)
        today = date.today()
        qs = DailyExerciseLog.objects.filter(client=client_profile, date=today)
        formset = DailyLogFormSet(request.POST, queryset=qs)
        if formset.is_valid():
            formset.save()
            return redirect('workouts:today_exercises')
        return render(request, self.template_name, {
            'today': today,
            'formset': formset,
        })