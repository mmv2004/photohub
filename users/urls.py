from django.urls import path
from django.contrib.auth.views import (
    LogoutView, 
)
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('', views.dashboard_view, name='dashboard'),
]

