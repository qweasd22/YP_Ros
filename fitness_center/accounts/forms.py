from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css = 'form-check-input'
            field.widget.attrs.update({
                'class': css,
                'placeholder': field.label,
            })
class RegisterForm(BootstrapFormMixin, UserCreationForm):
    full_name = forms.CharField(label='ФИО', max_length=200)
    phone = forms.CharField(label='Телефон', max_length=20)
    birth_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    gender = forms.ChoiceField(
        label='Пол',
        choices=(('M','Мужской'), ('F','Женский')),
        widget=forms.Select()
    )
    photo = forms.ImageField(label='Фото профиля', required=False)

    class Meta:
        model = User
        fields = ('full_name', 'phone', 'birth_date', 'gender', 'photo', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        user.phone = self.cleaned_data['phone']
        user.birth_date = self.cleaned_data['birth_date']
        user.gender = self.cleaned_data['gender']
        if self.cleaned_data.get('photo'):
            user.photo = self.cleaned_data['photo']
        user.role = 'client'
        if commit:
            user.save()
        return user


class LoginForm(BootstrapFormMixin, forms.Form):
    phone = forms.CharField(label='Телефон', max_length=20)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'phone', 'birth_date', 'gender', 'photo')
        widgets = {
            'full_name':    forms.TextInput(attrs={'class': 'form-control'}),
            'phone':        forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date':   forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'gender':       forms.Select(attrs={'class':'form-select'}),
            'photo':        forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

from django import forms
from django.contrib.auth import get_user_model
from clients.models import ClientProfile
from trainers.models import TrainerProfile

User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'phone', 'birth_date', 'gender', 'photo')
        widgets = {
            'full_name':  forms.TextInput(attrs={'class':'form-control'}),
            'phone':      forms.TextInput(attrs={'class':'form-control'}),
            'birth_date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'gender':     forms.Select(attrs={'class':'form-select'}),
            'photo':      forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ('trainer', 'discount')
        widgets = {
            'trainer': forms.Select(attrs={'class':'form-select'}),
            'discount': forms.NumberInput(attrs={'class':'form-control','step':'0.01','min':'0'}),
        }

class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ('experience_years', 'achievements')
        widgets = {
            'experience_years': forms.NumberInput(attrs={'class':'form-control','min':'0'}),
            'achievements':     forms.Textarea(attrs={'class':'form-control','rows':3}),
        }
