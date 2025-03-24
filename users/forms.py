from django.contrib.auth.forms import UserCreationForm

from users.models import User


# Адаптировать форму регистрации пользователя под кастомную модель пользователя
class UserRegisterForm(UserCreationForm):
    class Meta:
        # Указать модель, на основе которой будет создана форма
        model = User
        # Определить поля, которые будут включены в форму регистрации
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторите пароль'})