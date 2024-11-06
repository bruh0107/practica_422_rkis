from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import datetime

from .models import BookInstance

class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Неверная дата — продление в прошлом'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Неверная дата — продление более чем на 4 недели вперед'))

        return data

    class Meta:
        model = BookInstance
        fields = ['due_back',]
        labels = { 'due_back': _('Дата продления') }
        help_text = { 'due_back': _('Введите дату между текущим моментом и 4 неделями (по умолчанию 3).'), }

