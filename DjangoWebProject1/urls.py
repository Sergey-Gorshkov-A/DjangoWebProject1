"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('links/', views.links, name='links'),
    path('pool/', views.pool, name='pool'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Войти',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('registration/', views.registration, name='registration'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('newpost/', views.newpost, name='newpost'),
    path('videopost/', views.videopost, name='videopost'),
    path('catalog/', views.catalog, name='catalog'),
    path('service/<str:parametr>', views.service, name='service'),
    path('servicepost/<int:parametr>/', views.servicepost, name='servicepost'),
    path('newservice/', views.newservice, name='newservice'),
    path('basket/', views.basket, name='basket'),
    path('orderpost/<str:parametr>/', views.orderpost, name='orderpost'),
    path('order/', views.order, name='order'),
    path('editorder/<str:parametr>/', views.editorder, name='editorder'),
    path('completedorder/<str:parametr>/', views.completedorder, name='completedorder'),
    path('postedit/<int:parametr>/', views.postedit, name='postedit'),
    path('editservice/<int:parametr>/', views.editservice, name='editservice'),
    path('deletepost/<int:parametr>/', views.deletepost, name='deletepost'),
    path('deleteservice/<int:parametr>/', views.deleteservice, name='deleteservice'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
