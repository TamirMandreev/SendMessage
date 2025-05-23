from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from config.settings import EMAIL_HOST_USER
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from django.views.generic.detail import SingleObjectMixin

from dispatcher.forms import RecipientForm, MessageForm, MailingForm
from dispatcher.models import Recipient, Message, Mailing, AttemptToMailing


# Create your views here.
# 1. Управление клиентами


# Кэшировать результаты вызова метода dispatch на протяжении 60 секунд
@method_decorator(cache_page(60), name="dispatch")
class RecipientListView(ListView):
    """
    Представление для отображения всех получателей рассылки (клиентов)
    """

    model = Recipient
    template_name = "dispatcher/recipients_list.html"
    context_object_name = "recipients"

    # Настроить запрос к базе данных, который будет фильтровать
    # список получетелй рассылок по полю owner модели Recipient
    # Если у пользователя есть право просматривать всех получателей
    # рассылки, то возвращать всех получателей рассылки
    def get_queryset(self):
        try:
            # Получаем текущего пользователя
            user = self.request.user
            # Если у пользователя есть право can_view_all_clients
            if user.has_perm("dispatcher.can_view_all_clients"):
                return super().get_queryset()
            else:
                # Фильтруем queryset по полю owner
                queryset = super().get_queryset()
                return queryset.filter(owner=user)
        except Exception:
            return redirect(reverse_lazy("users:login"))


class RecipientCreateView(CreateView):
    """
    Представление для создания получателей рассылки (клиентов)
    """

    model = Recipient
    form_class = RecipientForm
    template_name = "dispatcher/recipient_form.html"
    success_url = reverse_lazy("dispatcher:recipients_list")

    # Метод form_valid вызывается после успешной проверки формы
    # Этот метод используется для выполнения каких-либо
    # действий перед сохранением формы
    def form_valid(self, form):
        # Установить значение поля owner
        form.instance.owner = self.request.user
        # Вызвать родительский метод
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования получателя рассылки (клиента)
    """

    model = Recipient
    form_class = RecipientForm
    template_name = "dispatcher/recipient_form.html"
    success_url = reverse_lazy("dispatcher:recipients_list")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.owner == self.request.user:
            return object
        else:
            return PermissionDenied(
                "У вас нет прав на редактирование этого получателя рассылки"
            )


# Кэшировать результаты вызова метода dispatch на протяжении 60 секунд
@method_decorator(cache_page(60), name="dispatch")
class RecipientDetailView(DetailView):
    """
    Представление для просмотра детальной информации о получателе
    рассылки (клиенте)
    """

    model = Recipient
    template_name = "dispatcher/recipient_detail.html"
    context_object_name = "recipient"

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.owner == self.request.user:
            return object
        else:
            return PermissionDenied(
                "У вас нет прав на просмотр этого получателя рассылки"
            )


class RecipientDeleteView(DeleteView):
    """
    Представление для удаления получателя рассылки (клиента)
    """

    model = Recipient
    template_name = "dispatcher/recipient_delete.html"
    success_url = reverse_lazy("dispatcher:recipients_list")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.owner == self.request.user:
            return object
        else:
            return PermissionDenied(
                "У вас нет прав на удаление этого получателя рассылки"
            )


# 2. Управление сообщениями


class MessageCreateView(CreateView):
    """
    Представление для создания сообщения
    """

    model = Message
    form_class = MessageForm
    template_name = "dispatcher/message_form.html"
    success_url = reverse_lazy("dispatcher:messages_list")

    # Метод form_valid вызывается после успешной проверки формы
    # Этот метод используется для выполнения каких-либо
    # действий перед сохранением формы
    def form_valid(self, form):
        # Установить значение поля owner
        form.instance.owner = self.request.user
        # Вызвать родительский метод
        return super().form_valid(form)


# Кэшировать результаты вызова метода dispatch на протяжении
# 60 секунд
@method_decorator(cache_page(60), name="dispatch")
class MessageListView(ListView):
    """
    Представление для отображения всех сообщений
    """

    model = Message
    template_name = "dispatcher/messages_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user
        # Получаем все сообщения
        queryset = super().get_queryset()
        # Фильтруем queryset по полю owner
        return queryset.filter(owner=user)



# Кэшировать результаты вызова метода dispatch на протяжении
# 60 секунд
@method_decorator(cache_page(60), name="dispatch")
class MessageDetailView(DetailView):
    """
    Представление для отображения подробной информации о сообщении
    """

    model = Message
    template_name = "dispatcher/message_detail.html"
    context_object_name = "message"


class MessageUpdateView(UpdateView):
    """
    Представление для редактирования сообщения
    """

    model = Message
    form_class = MessageForm
    template_name = "dispatcher/message_form.html"
    success_url = reverse_lazy("dispatcher:messages_list")


class MessageDeleteView(DeleteView):
    """
    Представление для удаления сообщения
    """

    model = Message
    template_name = "dispatcher/message_delete.html"
    success_url = reverse_lazy("dispatcher:messages_list")


# 3. Управление рассылками
# LoginRequiredMixin предоставляет доступ к этому
# представлению только авторизованным пользователям
class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания рассылки
    """

    model = Mailing
    form_class = MailingForm
    template_name = "dispatcher/mailing_form.html"
    success_url = reverse_lazy("dispatcher:mailings_list")

    # Метод form_valid вызывается после успешной проверки формы
    # Этот метод используется для выполнения каких-либо действий
    # перед сохранением формы
    def form_valid(self, form):
        # Установить значение поля owner
        form.instance.owner = self.request.user
        # Вызвать родительский метод
        return super().form_valid(form)


# Кэшировать результаты вызова метода dispatch на протяжении
# 60 секунд
@method_decorator(cache_page(60), name="dispatch")
class MailingListView(ListView):
    """
    Представление для отображения всех рассылок
    """

    model = Mailing
    template_name = "dispatcher/mailings_list.html"
    context_object_name = "mailings"

    # Настроить запрос к базе данных, который будет фильтровать
    # список рассылок по полю owner модели Mailing
    # Если у пользователя есть право просматривать все рассылки,
    # возвращать все рассылки
    def get_queryset(self):
        try:
            # Получаем текущего пользователя
            user = self.request.user
            # Если у пользователя есть право can_view_all_mailings
            if user.has_perm("dispatcher.can_view_all_mailings"):
                return super().get_queryset()
            else:
                # Фильтруем queryset по полю owner
                queryset = super().get_queryset()
                return queryset.filter(owner=user)
        except TypeError:
            return redirect(reverse_lazy("users:login"))


# Кэшировать результаты вызова метода dispatch на протяжении
# 60 секунд
@method_decorator(cache_page(60), name="dispatch")
class MailingDetailView(DetailView):
    """
    Представление для отображения подробной информации о рассылке
    """

    model = Mailing
    template_name = "dispatcher/mailing_detail.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        user = self.request.user
        if object.owner == self.request.user or user.has_perm(
            "dispatcher.can_view_all_mailings"
        ):
            return object
        else:
            return HttpResponse("У вас нет прав на просмотр этой рассылки")


class MailingUpdateView(UpdateView):
    """
    Представление для редактирования рассылки
    """

    model = Mailing
    form_class = MailingForm
    template_name = "dispatcher/mailing_form.html"
    success_url = reverse_lazy("dispatcher:mailings_list")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        user = self.request.user
        if object.owner == self.request.user or user.has_perm(
            "dispatcher.can_view_all_mailings"
        ):
            return object
        else:
            return HttpResponse(
                "У вас нет прав на редактирование этой рассылки"
            )


class MailingDeleteView(DeleteView):
    """
    Представление для удаления рассылки
    """

    model = Mailing
    template_name = "dispatcher/mailing_delete.html"
    success_url = reverse_lazy("dispatcher:mailings_list")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.owner == self.request.user:
            return object
        else:
            raise PermissionDenied("У вас нет прав на удаление этой рассылки")


# SingleIbjectMixin позволяет получать объект модели
# по идентификатору (id)
class MailingStartView(TemplateView, SingleObjectMixin):
    """
    Представление для обработки POST-запроса на запуск рассылки
    """

    # Указать модель, с которой будет работать представление
    model = Mailing
    # Указать имя аргумента URL, который содержит первичный ключ объекта
    pk_url_kwarg = "pk"
    template_name = "dispatcher/mailing_detail.html"
    context_object_name = "mailing"

    # Метод post обрабатывает POST-запросы.
    # Он вызывается, когда форма отправляется методом POST
    def post(self, request, *args, **kwargs):
        # Создать переменную для хранения количества успешных
        # отправок
        sent_count = 0

        # Получить объект модели Mailing по переданному id
        mailing = self.get_object()
        # Обновить статус рассылки
        mailing.status = mailing.LAUNCHED
        # Записать дату и время первой отправки
        if not mailing.date_time_of_first_mailing:
            mailing.date_time_of_first_mailing = timezone.now()
        # Сохранить изменения в базу данных
        mailing.save()

        # Создать объект модели AttemptToMailing
        attempt = AttemptToMailing.objects.create(
            date_time_of_attempt=timezone.now(),
            mailing=mailing,
            owner=self.request.user,
        )

        for email in mailing.get_recipients_for_mailing():
            try:
                # Отправить сообщения
                send_mail(
                    subject=mailing.message.theme,  # Тема письма
                    message=mailing.message.body,  # Тело письма
                    from_email=EMAIL_HOST_USER,  # Адрес отправителя
                    recipient_list=[email],  # Email получателя
                )
                # Установить статус отправки "Успешно"
                attempt.status = "1"
                # Увеличить счетчик успешных отправок
                sent_count += 1

            except Exception as e:
                # Установить статус отправки "Не успешно"
                attempt.status = "0"
                # Записать информацию об ошибке в "Ответ почтового сервера"
                attempt.mail_server_response = e

        # Записать количество отправленных сообщений
        attempt.messages_count += sent_count
        # Сохранить attempt
        attempt.save()

        # Записать дату и время окончания отправки
        mailing.date_time_end_mailing = timezone.now()
        # Обновить статус рассылки
        mailing.status = mailing.COMPLETED

        # Сохранить изменения
        mailing.save()

        # После успешной отправки письма перенаправить пользователя
        # обратно на страницу подробной информации о рассылке
        return HttpResponseRedirect(
            reverse_lazy(
                "dispatcher:mailing_detail", kwargs={"pk": mailing.pk}
            )
        )


# 4. Домашняя страница
class Home(TemplateView):
    model = Mailing
    template_name = "dispatcher/home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Количество всех рассылок
            number_of_mailings = (
                Mailing.objects.all().filter(owner=self.request.user).count()
            )
            # Количество активных рассылок
            number_of_active_mailings = Mailing.objects.filter(
                status=Mailing.LAUNCHED, owner=self.request.user
            ).count()
            # Количество уникальных получателей
            number_of_unique_recipient = (
                Recipient.objects.all()
                .distinct()
                .filter(owner=self.request.user)
                .count()
            )
            # Общее количество попыток рассылок
            number_of_attempts = AttemptToMailing.objects.filter(
                owner=self.request.user
            ).count()
            # Количество успешных попыток
            success_attempts = AttemptToMailing.objects.filter(
                owner=self.request.user, status="1"
            ).count()
            # Количество неуспешных попыток
            unsuccess_attempts = AttemptToMailing.objects.filter(
                owner=self.request.user, status="0"
            ).count()
            # Количество отправленных сообщений
            number_of_messages = AttemptToMailing.objects.filter(
                owner=self.request.user
            ).aggregate(total=Sum("messages_count"))["total"]

            context["number_of_mailings"] = number_of_mailings
            context["number_of_active_mailings"] = number_of_active_mailings
            context["number_of_unique_recipient"] = number_of_unique_recipient
            context["number_of_attempts"] = number_of_attempts
            context["success_attempts"] = success_attempts
            context["unsuccess_attempts"] = unsuccess_attempts
            context["number_of_messages"] = number_of_messages

            return context

        except TypeError:
            redirect(reverse_lazy("users:login"))


# Создать представление для отображения списка попыток рассылок
class AttemptToMailingListView(ListView):
    # Указать модель, с которой будет работать представление
    model = AttemptToMailing
    # Указать шаблон, который будет отображать список попыток рассылок
    template_name = "dispatcher/attemt_to_mailing_list.html"
    # Задать имя переменной, под которой список объектов будет
    # доступен в шаблоне
    context_object_name = "attempt_to_mailings"
