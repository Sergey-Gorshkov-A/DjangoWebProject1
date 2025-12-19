"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .models import Comment, Blog, Service, Order

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))


class PoolForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    question1 = forms.ChoiceField(label='Вам нравится содержание страниц сайта?',
                                  choices=(('1', 'Да'), ('2', 'Нет')), initial=1)
    question2 = forms.ChoiceField(label='Вам нравится офорление сайта?',
                                  choices=(('1', 'Да'), ('2', 'Нет'), ('3', 'Не очень')), initial=1)
    question3 = forms.ChoiceField(label='У вас есть машина?',
                                  choices=[('1', 'Да'), ('2', 'Нет')], widget=forms.RadioSelect, initial=1)
    question4 = forms.BooleanField(label='Вам нужен ремонт?', required=False)
    text = forms.CharField(label='Ваше мнение по поводу сайта',
                           widget=forms.Textarea(attrs={'rows':12, 'cols':30}))


class CommentForm (forms.ModelForm):
    
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text


class BlogForm (forms.ModelForm):

    class Meta:
        model = Blog # используемая модель
        fields = ('title', 'description', 'content', 'image',)
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}


class ServiceForm (forms.ModelForm):

    class Meta:
        model = Service # используемая модель
        fields = ('title', 'description', 'content', 'price', 'image', 'category',)
        labels = {'title': "Название услуги", 'description': "Краткое содержание", 'content': "Полное содержание", 'price': "Цена", 'image': "Картинка", 'category': "Категория"}


class OrderForm (forms.ModelForm):

    class Meta:
        model = Order # используемая модель
        fields = ('confrim',)
        labels = {'confrim': "Подтверждение заказа"}
