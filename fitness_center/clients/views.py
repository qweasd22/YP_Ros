from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from trainers.models import TrainerProfile
from .forms import ApplicationForm
from trainers.models import TrainingApplication
from django.shortcuts import get_object_or_404

class TrainerListView(LoginRequiredMixin, generic.ListView):
    model = TrainerProfile
    template_name = 'clients/trainer_list.html'
    context_object_name = 'trainers'

class ApplicationCreateView(LoginRequiredMixin, generic.CreateView):
    model = TrainingApplication
    form_class = ApplicationForm
    template_name = 'clients/trainer_apply.html'

    def dispatch(self, request, *args, **kwargs):
        self.trainer = get_object_or_404(TrainerProfile, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        app = form.save(commit=False)
        app.client = self.request.user.clientprofile
        app.trainer = self.trainer
        app.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('clients:application_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['trainer'] = self.trainer
        return ctx

class ApplicationListView(LoginRequiredMixin, generic.ListView):
    model = TrainingApplication
    template_name = 'clients/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return TrainingApplication.objects.filter(client=self.request.user.clientprofile).order_by('-created_at')
