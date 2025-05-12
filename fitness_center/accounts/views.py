from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views import View
from .forms import RegisterForm, LoginForm

def home(request):
    return render(request, 'accounts/home.html')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request, phone=phone, password=password)
            if user:
                login(request, user)
                return redirect('home')
            form.add_error(None, 'Неверный телефон или пароль.')
        return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, TrainerProfileForm
from clients.models import ClientProfile
from trainers.models import TrainerProfile
from datetime import date

class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        user = request.user
        user_form = UserForm(instance=user)
        trainer_form = None
        client_profile = None

        if user.role == 'trainer':
            trainer_form = TrainerProfileForm(instance=getattr(user, 'trainerprofile', None))
        elif user.role == 'client':
            client_profile = getattr(user, 'clientprofile', None)

        return render(request, self.template_name, {
            'user_form': user_form,
            'trainer_form': trainer_form,
            'client_profile': client_profile,
        })

    def post(self, request):
        user = request.user
        user_form = UserForm(request.POST, request.FILES, instance=user)
        saved = False

        if user_form.is_valid():
            user_form.save()
            saved = True

        if saved:
            return redirect('accounts:profile')

        # при ошибках показываем формы снова
        trainer_form = None
        client_profile = None
        if user.role == 'trainer':
            trainer_form = TrainerProfileForm(request.POST, instance=getattr(user, 'trainerprofile', None))
        elif user.role == 'client':
            client_profile = getattr(user, 'clientprofile', None)

        return render(request, self.template_name, {
            'user_form': user_form,
            'trainer_form': trainer_form,
            'client_profile': client_profile,
        })
