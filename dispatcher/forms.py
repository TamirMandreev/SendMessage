from django.forms import ModelForm
from dispatcher.models import Recipient, Message


class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите email'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ФИО'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': ''})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['theme'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите тему'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Сообщение'})
