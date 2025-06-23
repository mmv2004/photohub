from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView

from .forms import (
    CustomUserCreationForm, 
    CustomUserChangeForm, 
    CustomAuthenticationForm,
)
from .models import CustomUser

# Функция для проверки, является ли пользователь администратором
def is_admin(user):
    return user.is_staff or user.is_superuser

class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя
    """
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        # Сохраняем пользователя
        response = super().form_valid(form)
        # Автоматически авторизуем пользователя после регистрации
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(self.request, user)
        messages.success(self.request, 'Регистрация успешно завершена!')
        return response
    
    def dispatch(self, request, *args, **kwargs):
        # Если пользователь уже авторизован, перенаправляем на дашборд
        if request.user.is_authenticated:
            return redirect('users:dashboard')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    """
    Представление для авторизации пользователя
    """
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('users:dashboard')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профиля пользователя
    """
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    login_url = reverse_lazy('users:login')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)


@login_required(login_url='users:login')
def dashboard_view(request):
    return redirect(to="calendar:calendar")

# Представление для администраторов
@user_passes_test(is_admin, login_url='users:login')
def admin_dashboard_view(request):
    """
    Представление для административной панели
    """
    # Получаем всех пользователей
    users = CustomUser.objects.all().order_by('-date_joined')[:10]
    
    # Получаем все студии
    from studios.models import Studio
    studios = Studio.objects.all().order_by('-created_at')[:10]
    
    context = {
        'users': users,
        'studios': studios,
    }
    
    return render(request, 'users/admin_dashboard.html', context)

