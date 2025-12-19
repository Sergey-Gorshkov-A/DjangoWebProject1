"""
Definition of views.
"""

from datetime import datetime
from pickle import TRUE
from unicodedata import category
import weakref
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app.forms import PoolForm, CommentForm, BlogForm, ServiceForm, OrderForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog, Comment, Service, Order

def home(request):
    """Renders the home page."""
    last_posts = Blog.objects.all().order_by('-posted')[:3]
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'last_posts': last_posts,
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Ссылки на похожие сайты.',
            'year':datetime.now().year,
        }
    )

def pool(request):
    assert isinstance(request, HttpRequest)
    data = None
    question1 = {'1': 'Да', '2': 'Нет'}
    question2 = {'1': 'Да', '2': 'Нет', '3': 'Не очень'}
    question3 = {'1': 'Да', '2': 'Нет'}

    if request.method == 'POST':
        form = PoolForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['question1'] = question1[ form.cleaned_data['question1'] ]
            data['question2'] = question2[ form.cleaned_data['question2'] ]
            data['question3'] = question3[ form.cleaned_data['question3'] ]
            if (form.cleaned_data['question4'] == True):
                data['question4'] = 'Да'
            else:
                data['question4'] = 'Нет'
            data['text'] = form.cleaned_data['text']
            
            form = None
    else:
        form = PoolForm()
    return render(
        request,
        'app/pool.html',
        {
            'title':"Форма отзыва",
            'form':form,
            'data':data,
            'year':datetime.now().year,
         }
    )

def registration(request):
    """Renders the registration page."""
    
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    
    assert isinstance(request, HttpRequest)
    return render(
           request,
           'app/registration.html',
            {
                'regform': regform, # передача формы в шаблон веб-страницы
                'year':datetime.now().year,
            }
        )

def blog(request):
    
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()
    return render(
        request,
        'app/blog.html',
        {
            'title':'Новости',
            'posts': posts,
            'year':datetime.now().year,
            }
        )


def blogpost(request, parametr):
    
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=post_1)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)

            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)

            comment_f.save()

            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1':post_1,
            'comments': comments,
            'form': form,
            'year':datetime.now().year,
            }
        )


def newpost(request):

    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()
    
    return render(
         request,
         'app/newpost.html',
          {
                'blogform':blogform,
                'title':'Добавить новостную статью',

                'year':datetime.now().year,
                }
            )


def videopost(request):
    """Renders the video page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )


def catalog(request):
    
    categories = ["Техническое обслуживание", "Ремонт кузовных деталей", "Мойка и чистка автомобиля"]
    
    assert isinstance(request, HttpRequest)
    
    return render(
        request,
        'app/catalog.html',
        {
            'title':'Категории услуг',
            'categories': categories,
            'year':datetime.now().year,
            }
        )


def service(request, parametr):
    
    services = Service.objects.filter(category=parametr)
    assert isinstance(request, HttpRequest)
    
    return render(
        request,
        'app/service.html',
        {
            'title':'Каталог услуг',
            'services': services,
            'year':datetime.now().year,
            }
        )


def servicepost(request, parametr):
    
    service_1 = Service.objects.get(id=parametr)
    
    if request.method == "POST":
        order_1 = Order()
        order_1.customer = request.user
        order_1.service = service_1
        order_1.price = service_1.price
        order_1.save()
        return redirect('catalog')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/servicepost.html',
        {
            'title':"Страница услуги",
            'service_1':service_1,
            'year':datetime.now().year,
            }
        )


def newservice(request):

    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        serviceform = ServiceForm(request.POST, request.FILES)
        if serviceform.is_valid():
            service_f = serviceform.save(commit=False)
            service_f.save()

            return redirect('service')
    else:
        serviceform = ServiceForm()
    
    return render(
         request,
         'app/newservice.html',
          {
                'serviceform':serviceform,
                'title':'Добавить услугу',

                'year':datetime.now().year,
                }
            )


def basket(request):
    
    orders = Order.objects.filter(customer=request.user)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/basket.html',
        {
            'title':'Мои заказы',
            'orders': orders,
            'year':datetime.now().year,
            }
        )


def orderpost(request, parametr):
    
    order_1 = Order.objects.get(ordered=parametr)
    
    if request.method == "POST":
        Order.objects.filter(ordered=order_1.ordered).delete()
        return redirect('basket')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/orderpost.html',
        {
            'title':order_1.service.title,
            'order_1':order_1,
            'year':datetime.now().year,
            }
        )


def order(request):
    
    assert isinstance(request, HttpRequest)
    orders = Order.objects.all()

    return render(
        request,
        'app/order.html',
        {
            'title':'Заказы клиентов',
            'orders': orders,
            'year':datetime.now().year,
            }
        )


def editorder(request, parametr):
    
    order_1 = Order.objects.get(ordered=parametr)
    
    if request.method == "POST":
        if not order_1.confrim:
            order_1.confrim = True
        else:
            order_1.confrim = False
        order_1.save()
        return redirect('order')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/editorder.html',
        {
            'title':order_1.service.title,
            'order_1':order_1,
            'year':datetime.now().year,
            }
        )


def completedorder(request, parametr):
    
    order_1 = Order.objects.get(ordered=parametr)
    
    if request.method == "POST":
        order_1.completed = True
        order_1.save()
        return redirect('order')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/completedorder.html',
        {
            'title':order_1.service.title,
            'order_1':order_1,
            'year':datetime.now().year,
            }
        )


def postedit(request, parametr):
    post_1 = Blog.objects.get(id=parametr)

    if request.method == "POST":
        form = BlogForm(request.POST, instance=post_1)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogForm(instance=post_1)
    return render (
        request,
        'app/postedit.html',
        {
            'post_1':post_1,
            'form': form,
            'year':datetime.now().year,
            }
        )


def editservice(request, parametr):
    service_1 = Service.objects.get(id=parametr)

    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service_1)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ServiceForm(instance=service_1)
    return render (
        request,
        'app/editservice.html',
        {
            'service_1':service_1,
            'form': form,
            'year':datetime.now().year,
            }
        )