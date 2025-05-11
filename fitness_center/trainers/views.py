from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import TrainerProfile, TrainingApplication
from .forms import ApplicationActionForm, TrainingPlanForm, PlanExerciseFormSet

class DashboardView(LoginRequiredMixin, generic.ListView):
    model = TrainingApplication
    template_name = 'trainers/dashboard.html'
    context_object_name = 'applications'

    def get_queryset(self):
        tp = get_object_or_404(TrainerProfile, user=self.request.user)
        return tp.applications.filter(status='pending').order_by('created_at')

from django.utils import timezone
class ApplicationDetailView(LoginRequiredMixin, generic.View):
    template_name = 'trainers/application_detail.html'

    def get(self, request, pk):
        app = get_object_or_404(TrainingApplication, pk=pk, trainer__user=request.user)
        form = ApplicationActionForm(instance=app)
        return render(request, self.template_name, {'application': app, 'form': form})

    def post(self, request, pk):
        app = get_object_or_404(TrainingApplication, pk=pk, trainer__user=request.user)
        form = ApplicationActionForm(request.POST, instance=app)
        if form.is_valid():
            app = form.save(commit=False)
            app.responded_at = timezone.now()
            app.save()
            if app.status == 'accepted':
                return redirect('trainers:plan_create', pk=app.pk)
            return redirect('trainers:dashboard')
        return render(request, self.template_name, {'application': app, 'form': form})


class PlanCreateView(LoginRequiredMixin, generic.View):
    template_name = 'trainers/plan_create.html'

    def get(self, request, pk):
        app = get_object_or_404(TrainingApplication, pk=pk, trainer__user=request.user, status='accepted')
        plan_form = TrainingPlanForm()
        formset = PlanExerciseFormSet()
        return render(request, self.template_name, {'application': app, 'plan_form': plan_form, 'formset': formset})

    def post(self, request, pk):
        app = get_object_or_404(TrainingApplication, pk=pk, trainer__user=request.user, status='accepted')
        plan_form = TrainingPlanForm(request.POST)
        formset = PlanExerciseFormSet(request.POST)
        if plan_form.is_valid() and formset.is_valid():
            plan = plan_form.save(commit=False)
            plan.client = app.client  # ВАЖНО: берём клиента из заявки, а не из request.user!
            plan.save()
            formset.instance = plan
            formset.save()
            return redirect('clients:application_list')
        return render(request, self.template_name, {'application': app, 'plan_form': plan_form, 'formset': formset})

