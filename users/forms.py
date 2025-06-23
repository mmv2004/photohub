from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm,  SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from datetime import date
from dateutil.relativedelta import relativedelta


class CustomUserCreationForm(UserCreationForm):
    """
    Форма для создания нового пользователя с дополнительными полями
    """
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    first_name = forms.CharField(
        label=_("Имя"),
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
    )
    last_name = forms.CharField(
        label=_("Фамилия"),
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
    )
    birth_date = forms.DateField(
        label=_("Дата рождения"),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
    )
    avatar = forms.ImageField(
        label=_("Аватар"),
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}),
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'birth_date', 'avatar', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.birth_date = self.cleaned_data['birth_date']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        max_birth_date = date.today() - relativedelta(years=14)
        self.fields['birth_date'].widget.attrs['max'] = max_birth_date.strftime('%Y-%m-%d')

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 14:
                raise ValidationError("Клиент должен быть не младше 14 лет.")
        return birth_date

class CustomUserChangeForm(UserChangeForm):
    """
    Форма для изменения данных пользователя
    """
    password = None  # Удаляем поле пароля из формы
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'birth_date', 'avatar', 'phone_number')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    """
    Форма для аутентификации пользователя
    """
    username = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
    )


class CustomSetPasswordForm(SetPasswordForm):
    """
    Форма для установки нового пароля
    """
    new_password1 = forms.CharField(
        label=_("Новый пароль"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}),
    )
    new_password2 = forms.CharField(
        label=_("Подтверждение нового пароля"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение нового пароля'}),
    )

