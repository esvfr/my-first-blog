# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

#from urllib.parse import urlparse
from urlparse import urlparse

from django.shortcuts import redirect, render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.utils import timezone
from django.views import View
from django.contrib.auth.forms import AuthenticationForm

#from accounts.models import TemporaryBanIp
from .models import TemporaryBanIp
from .special_func import get_next_url, get_client_ip


class ELoginView(View):
    def get(self, request):
        # если пользователь авторизован, то делаем редирект на главную страницу
        if auth.get_user(request).is_authenticated:
            return redirect('/blog')
        else:
            # Иначе формируем контекст с формой авторизации и отдаём страницу
            # с этим контекстом.
            # работает, как для url - /admin/login/ так и для /accounts/login/
            context = create_context_username_csrf(request)
            return render_to_response('accounts/login.html', context=context)

    def post(self, request):
        # получив запрос на авторизацию
        form = AuthenticationForm(request, data=request.POST)

        # забираем IP адрес из запроса
        ip = get_client_ip(request)

        # получаем или создаём новую запись об IP, с которого вводится пароль, на предмет блокировки
        obj, created = TemporaryBanIp.objects.get_or_create(
            defaults={
                'ip_address': ip,
                'time_unblock': timezone.now()
            },
            ip_address=ip
        )

        # если IP заблокирован и время разблокировки не настало
        if obj.status is True and obj.time_unblock > timezone.now():
            context = create_context_username_csrf(request)
            if obj.attempts == 3 or obj.attempts == 6:
                # то открываем страницу с сообщением о блокировки на 15 минут при 3 и 6 неудачных попытках входа
                return render_to_response('accounts/block_15_minutes.html', context=context)
            elif obj.attempts == 9:
                # или открываем страницу о блокировке на 24 часа, при 9 неудачных попытках входа
                return render_to_response('accounts/block_24_hours.html', context=context)
        elif obj.status is True and obj.time_unblock < timezone.now():
            # если IP заблокирован, но время разблокировки настало, то разблокируем IP
            obj.status = False
            obj.save()

        # проверяем правильность формы, что есть такой пользователь
        # и он ввёл правильный пароль
        # если пользователь ввёл верные данные, то авторизуем его и удаляем запись о блокировке IP
        if form.is_valid():
            # в случае успеха авторизуем пользователя
            auth.login(request, form.get_user())
            #obj.attempts=0
            #obj.save()
            obj.delete()

            # получаем предыдущий url
            next = urlparse(get_next_url(request)).path
            # и если пользователь из числа персонала и заходил через url /admin/login/
            # то перенаправляем пользователя в админ панель
            if next == '/admin/login/' and request.user.is_staff:
                return redirect('/admin/')
            # иначе делаем редирект на предыдущую страницу,
            # в случае с /accounts/login/ произойдёт ещё один редирект на главную страницу
            # в случае любого другого url, пользователь вернётся на данный url
            return redirect(next)
        else:
            # иначе считаем попытки и устанавливаем время разблокировки и статус блокировки
            obj.attempts += 1
            if obj.attempts == 3 or obj.attempts == 6:
                obj.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
                obj.status = True
            elif obj.attempts == 9:
                obj.time_unblock = timezone.now() + timezone.timedelta(1)
                obj.status = True
            elif obj.attempts > 9:
                obj.attempts = 1
            obj.save()

        # если данные не верны, то пользователь окажется на странице авторизации
        # и увидит сообщение об ошибке
        context = create_context_username_csrf(request)
        context['login_form'] = form

        return render_to_response('accounts/login.html', context=context)


# вспомогательный метод для формирования контекста с csrf_token
# и добавлением формы авторизации в этом контексте
def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context['login_form'] = AuthenticationForm
    return context
