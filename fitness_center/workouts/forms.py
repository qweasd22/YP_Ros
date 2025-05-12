from django import forms
from django.forms import modelformset_factory
from .models import DailyExerciseLog, PlanExercise

class DailyExerciseLogForm(forms.ModelForm):
    completed = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    heart_rate = forms.IntegerField(required=False, min_value=30, max_value=220)

    class Meta:
        model = DailyExerciseLog
        fields = ('completed', 'heart_rate')

# Formset по упражнениям плана
from django import forms
from django.forms import modelformset_factory
from workouts.models import DailyExerciseLog

DailyLogFormSet = modelformset_factory(
    DailyExerciseLog,
    fields=('completed', 'heart_rate',),
    extra=0,
    widgets={
        'completed':  forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': 30, 'max': 220}),
    }
)
