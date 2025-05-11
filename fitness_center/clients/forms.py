from django import forms
from trainers.models import TrainingApplication

class ApplicationForm(forms.ModelForm):
    goal = forms.CharField(
        label='Ваша цель',
        widget=forms.Textarea(attrs={'rows': 3})
    )

    class Meta:
        model = TrainingApplication
        fields = ('goal',)
