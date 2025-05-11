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
