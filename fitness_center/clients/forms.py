from django import forms
from trainers.models import TrainingApplication
from trainers.models import TrainingApplication
from django.forms import ModelForm
class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            cls = 'form-check-input' if isinstance(f.widget, forms.CheckboxInput) else 'form-control'
            f.widget.attrs.update({'class': cls, 'placeholder': f.label})

class ApplicationForm(BootstrapFormMixin, ModelForm):
    goal = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), label='Цель')
    class Meta:
        model = TrainingApplication
        fields = ['goal']

from django import forms
from trainers.models import TrainerProfile
from trainers.models import TrainingApplication

class TrainerChangeForm(forms.ModelForm):
    class Meta:
        model = TrainingApplication
        fields = ['trainer', 'goal']
        widgets = {
            'goal': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'trainer': forms.Select(attrs={'class': 'form-select'}),
        }

