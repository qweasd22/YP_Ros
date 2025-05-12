from django import forms
from django.forms import inlineformset_factory
from .models import TrainingApplication
from workouts.models import TrainingPlan, PlanExercise
from workouts.models import Exercise

class ApplicationActionForm(forms.ModelForm):
    # статус и причина отказа
    status = forms.ChoiceField(
        choices=TrainingApplication.STATUS_CHOICES,
        widget=forms.RadioSelect
    )
    reject_reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows':2}),
        required=False
    )

    class Meta:
        model = TrainingApplication
        fields = ('status', 'reject_reason')


class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ['start_date']

PlanExerciseFormSet = inlineformset_factory(
    TrainingPlan,
    PlanExercise,
    fields=['exercise', 'sets', 'reps','frequency_per_week'],
    extra=5,
    can_delete=False
)
