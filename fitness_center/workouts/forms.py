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
DailyLogFormSet = modelformset_factory(
    DailyExerciseLog,
    form=DailyExerciseLogForm,
    extra=0
)
