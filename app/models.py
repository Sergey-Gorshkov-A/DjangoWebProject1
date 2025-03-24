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

admin.site.register(Blog)
admin.site.register(Comment)