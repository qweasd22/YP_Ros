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
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = TrainingPlan
        fields = ('start_date',)

# набор упражнений внутри плана
PlanExerciseFormSet = inlineformset_factory(
    TrainingPlan, PlanExercise,
    fields=('exercise','frequency_per_week','sets','repetitions'),
    extra=3, can_delete=False,
    widgets={
      'exercise': forms.Select(),
      'frequency_per_week': forms.NumberInput(attrs={'min':1}),
      'sets': forms.NumberInput(attrs={'min':1}),
      'repetitions': forms.NumberInput(attrs={'min':1}),
    }
)
