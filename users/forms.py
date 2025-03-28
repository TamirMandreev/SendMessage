from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)

from users.models import User


# Адаптировать форму регистрации пользователя под кастомную модель пользователя
class UserRegisterForm(UserCreationForm):
    class Meta:
        # Указать модель, на основе которой будет создана форма
        model = User
        # Определить поля, которые будут включены в форму регистрации
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторите пароль"}
        )


# Стилизовать форму аутентификации пользователя
class UserAuthForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserAuthForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )


# Адаптировать форму регистрации пользователя под кастомную модель пользователя
class UserUpdateForm(UserCreationForm):
    class Meta:
        # Указать модель, на основе которой будет создана форма
        model = User
        # Определить поля, которые будут включены в форму регистрации
        fields = ["email", "image", "phone", "country"]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["image"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Загрузите изображение"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите телефон"}
        )
        self.fields["country"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите страну"}
        )
