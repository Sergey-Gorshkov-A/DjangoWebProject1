"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):

    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default='temp.jpg', verbose_name='Путь к картинке')

    # Методы класса:

    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self): 
        return self.title

    # Метаданные – вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Posts" # имя таблицы для модели
        ordering = ["-posted"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога" # тоже для всех статей блога


class Comment(models.Model):

    text = models.TextField(verbose_name="Текст")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Дата публикации")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    post = models.ForeignKey(Blog, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Пост")

    def __str__(self): 
        return self.text

    class Meta:
        db_table = "Comments" # имя таблицы для модели
        ordering = ["-date"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "комментарий" # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "комментарии" # тоже для всех статей блога


class Service(models.Model):

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    price = models.IntegerField(default=0, verbose_name="Цена")
    image = models.FileField(default='temp.jpg', verbose_name='Путь к картинке')
    category = models.CharField(default='', max_length=100, verbose_name="Категория")

    def get_absolute_url(self):
        return reverse("servicepost", args=[str(self.id)])

    def __str__(self): 
        return self.title

    class Meta:
        db_table = "Services" # имя таблицы для модели
        ordering = ["-price"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "услуга"
        verbose_name_plural = "услуги" 


class Order(models.Model):
    
    service = models.ForeignKey(Service, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Услуга")
    customer = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Покупатель")
    confrim = models.BooleanField(default=False, verbose_name="Подтвержден")
    ordered = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Заказан")
    price = models.IntegerField(default=0, verbose_name="Цена")
    completed = models.BooleanField(default=False, verbose_name="Завершен")
    
    def get_absolute_url(self):
        return reverse("orderpost", args=[str(self.id)])

    class Meta:
        db_table = "Orders" # имя таблицы для модели
        ordering = ["-id"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "заказ"
        verbose_name_plural = "заказы"


class Review(models.Model):
    RATING_CHOICES = [
        (1, 'Плохо'),
        (2, 'Удовлетворительно'),
        (3, 'Нормально'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    ]

    service = models.ForeignKey(Service, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Услуга")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=3, verbose_name = "Оценка")
    comment = models.TextField(blank=True, null=True, verbose_name = "Комментарий")
    created = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Создан")
    updated = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Изменён")

    def __str__(self):
        return f'Отзыв от {self.author.username} на {self.service.title}'

    def get_absolute_url(self):
        return reverse("reviewpost", args=[str(self.id)])

    class Meta:
        db_table = "Reviews" # имя таблицы для модели
        ordering = ["-id"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"


admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Review)
