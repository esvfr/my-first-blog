# -*- coding: utf-8 -*-
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin

from accounts.views import ELoginView  # Представление для авторизации из модуля accounts

from home.views import e_handler404, e_handler500  # For Error 404 500
from home import views

handler404 = e_handler404
handler500 = e_handler500

urlpatterns = [
    url(r'^admin/login/', ELoginView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),  # также добавим url модуля авторизаций
    url(r'^blog/', include('blog.urls')),
    url(r'^blog_list/', include('blog_list.urls')),
    url(r'^post/', include('post.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^api/', include('ajax.urls')),
    url(r'^', include('home.urls')),
    #    url(r'^$', views.EIndexView.as_view()),
]
