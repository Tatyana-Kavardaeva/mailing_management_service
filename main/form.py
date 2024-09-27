from django.forms import ModelForm, BooleanField, CharField
from django import forms
from main.models import Mailing, Client, Message, MailingLog


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


# class DateTimeInput(forms.DateTimeInput):
#     input_type = "datetime-local"
#
#     def __init__(self, **kwargs):
#         kwargs["format"] = "%Y-%m-%dT%H:%M"
#         super().__init__(**kwargs)


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ('is_active', 'status', 'owner')


    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word.lower() in cleaned_data.lower():
                raise forms.ValidationError('Ошибка, связанная с именем рассылки')
            return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word.lower() in cleaned_data.lower():
                raise forms.ValidationError('В описание продукта добавлены недопустимые слова')
            return cleaned_data


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word.lower() in cleaned_data.lower():
                raise forms.ValidationError('Ошибка, связанная с именем клиента')
            return cleaned_data


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)

    # def clean_title(self):
    #     cleaned_data = self.cleaned_data.get('name')
    #     forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
    #                        'радар']
    #     for word in forbidden_words:
    #         if word.lower() in cleaned_data.lower():
    #             raise forms.ValidationError('Ошибка, связанная с именем рассылки')
    #         return cleaned_data


class MailingLogForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MailingLog
        fields = '__all__'


class MailingManagerForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = ('is_active',)
