import secrets


from django.contrib.auth import login
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.cache import cache
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, ListView, DetailView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


# Создать представление для создания пользователя (Объекта модели User)
class UserCreateView(CreateView):
    # Указать модель, с которой будет работать представлением
    model = User
    # Указать шаблон, который будет использоваться для отображения
    # формы
    template_name = "users/user_create.html"
    # Интегрировать (подключить) form_class
    form_class = UserRegisterForm
    # Определить URL-адрес, на который будет перенаправлен
    # пользователь после успешной отправки формы
    success_url = reverse_lazy("users:login")

    # Метод form_valid вызывается после успешного заполнения формы
    # регистрации.
    # В нем мы выполняем дополнительные действия перед сохранением
    # нового пользователя
    def form_valid(self, form):
        # Сохранить данные формы. Создается новый экземпляр модели User
        user = form.save(commit=False)
        # Отключить статус активности пользователя
        user.is_active = False
        # Сгенерировать токен
        token = secrets.token_hex()
        # Присвоить токен пользователю
        user.token = token
        # Сохранить объект в базу данных
        user.save()

        # Получить полное доменное имя (хостнейм)
        host = self.request.get_host()
        # Создать ссылку для подтверждения почты
        url = f"http://{host}/users/email-confirm/{token}/"

        # Отправить письмо для подтверждения почты
        # Функция send_mail используется для отправки электронного
        # письма через SMTP-сервер
        send_mail(
            subject="Подтверждение почты",  # Заголовок письма
            # Тело письма
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,  # Адрес отправителя
            recipient_list=[user.email],  # Список получателей
        )

        # Вернуть результат работы базовой реализации метода form_valid
        return super().form_valid(form)


# Написать функцию, которая будет подтверждать почту пользователя
def email_verifivation(request, token):
    # Получить объект модели User по полю token
    user = get_object_or_404(User, token=token)
    # Активировать аккаунт пользователя
    user.is_active = True
    # Сохранить изменения
    user.save()

    # Перенаправить пользователя на страницу входа
    return redirect(reverse("users:login"))


# Создать представление для обработки запросов на восстановление пароля
# Его цель - предоставить пользователю форму для ввода своего
# email-адреса,
# проверить наличиего этого email-адреса в базе данных
# и отправить пользователю
# письмо с инструкциями по сбросу пароля
class PasswordResetRequestView(FormView):
    # Указать шаблон, который будет использоваться для о
    # тображения формы
    template_name = "users/password_reset_request.html"
    # Интегрировать (подключить) form_class
    form_class = PasswordResetForm
    # Определить URL-адрес, на который будет перенаправлен
    # пользователь после успешной отправки формы
    success_url = reverse_lazy("users:password_reset_confirm")

    # Метод form_valid вызывается, когда форма успешно
    # прошла валидацию (то есть пользователь ввел корректный
    # email-адрес)
    def form_valid(self, form):
        email = form.cleaned_data["email"]

        # Проверяем, существует ли пользователь с таким email
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            # Генерируем уникальный токен для сброса пароля
            reset_token = secrets.token_hex()
            user.reset_password_token = reset_token
            user.save()

            # Формируем ссылку для сброса пароля
            host = self.request.get_host()
            password_reset_link = (
                f"http://{host}/password-reset/{reset_token}/"
            )

            # Отправляем электронное письмо
            send_mail(
                subject="Запрос на восстановление пароля",
                message=f"Вы получили это письмо, потому что запросили "
                        f"восстановление пароля. Пожалуйста, пройдите по "
                        f"следующей ссылке для завершения процесса:"
                        f" {password_reset_link}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
            )

        return super().form_valid(form)


# Создать представление для сброса пароля
class PasswordResetView(FormView):
    # Указать шаблон, который будет использоваться
    # для отображения формы
    template_name = "users/password_reset.html"
    # Интегировать (подключить) form_class
    form_class = SetPasswordForm
    # Определить URL-адрес, на который будет перенаправлен
    # пользователь после сброса пароля
    success_url = reverse_lazy("users:home")

    # Метод dispatch вызывается перед каждым запросом к
    # представлению
    # Его цель - опеределить, какой пользователь запрашивает
    # сброс пароля, и проверить валидность токена
    def dispatch(self, request, *args, **kwargs):
        # Получить токен для сброса пароля
        reset_token = kwargs.get("reset_token")
        try:
            # Найти пользователя по токену
            user = User.objects.get(reset_token=reset_token)
        except User.DoesNotExist:
            raise Http404("Недействительный токен")

        # Сохранить пользователя в переменной экземпляра,
        # чтобы его можно было передать в форму
        self.user = user
        return super().dispatch(request, *args, **kwargs)

    # Метод get_form_kwargs используется для передачи
    # дополнительных аргументов в конструктор формы
    def get_form_kwargs(self):
        # Получить базовые аргументы из родительского класса
        kwargs = super().get_form_kwargs()
        # Добавить к полученным аргументам текущего пользователя
        kwargs["user"] = self.user
        # Вернуть объединенные аргументы
        return kwargs

    # Метод form_valid вызывается после успешного заполнения формы
    def form_valid(self, form):
        # Сохранить данные из формы в базу данных
        form.save()
        # Удалить токен для сброса пароля из экземпляра пользователя
        del self.user.reset_token
        # Сохранить обновленные данные
        self.user.save()
        # Метод login из пакета django.contrib.auth используется
        # для автоматической авторизации пользователя сразу после
        # успешного восстановления пароля
        login(self.request, self.user)
        # Вызвать родительский метод
        return super().form_valid(form)


# Создать представление для просмотра списка пользователей
class UsersListView(LoginRequiredMixin, ListView):
    # Указать модель, с которой будет работать представление
    model = User
    # Указать шаблон, который будет использоваться для о
    # тображения списка пользователей
    template_name = "users/users_list.html"
    # Задать имя переменной, под которой список объектов
    # будет доступен в шаблоне
    context_object_name = "users"

    # Настроить запрос получения списка пользователей к базе данных
    def get_queryset(self):
        # Получить пользователя, который отправляет запрос
        user = self.request.user
        # Если у пользователя нет права can_view_all_users
        if not user.has_perm("users.can_view_all_users"):
            return HttpResponseForbidden(
                "У вас нет права на просмотр списка пользователей"
            )

        # Получить queryset из кэша
        queryset = cache.get("users_queryset")
        # Если queryset пуст
        if queryset is None:
            queryset = User.objects.all()
            cache.set("users_queryset", queryset, 60)

        return queryset


# Создать представление для просмотра детальной информации о пользователе
class UserDetailView(LoginRequiredMixin, DetailView):
    # Указать модель, с которой будет работать представление
    model = User
    # Указать шаблон, который будет использоваться для отображения детальной информации о пользователе
    template_name = "users/user_detail.html"
    # Указать имя контекста
    context_object_name = "user"


# Создать представление для редактирования пользователя
class UserUpdateView(LoginRequiredMixin, UpdateView):
    # Указать модель, с которой будет работать представление
    model = User
    # Указать шаблон для редактирования пользователя
    template_name = "users/user_create.html"
    # Подключить form_class
    form_class = UserUpdateForm
    # Перенаправить на список пользователей
    success_url = reverse_lazy("users:users_list")


# Создать представление для блокировки пользователя
def block_user(request, pk):
    # Получить пользователя
    user = get_object_or_404(User, pk=pk)
    # Если пользователь имеет право can_block_users
    if user.has_perm("user.can_block_users"):
        # Установить поле is_active=False
        user.is_active = False
        # Сохранить пользователя
        user.save()
        return HttpResponse("Пользователь заблокирован")
    else:
        return HttpResponse("У вас нет права на блокировку пользователя")
