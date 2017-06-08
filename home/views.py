# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
#from django.contrib.syndication.views import Feed #For RSS
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import *

# Представление сделано на основе класса View
class EIndexView(View):
    def get(self, request):
        context = {}
        # Забираем все опубликованные статье отсортировав их по дате публикации
        all_articles = Article.objects.filter(article_status=True).order_by('-article_date')
        # Создаём Paginator, в который передаём статьи и указываем,
        # что их будет 10 штук на одну страницу
        current_page = Paginator(all_articles, 10)

        # Pagination в django_bootstrap3 посылает запрос вот в таком виде:
        # "GET /?page=2 HTTP/1.0" 200,
        # Поэтому нужно забрать page и попытаться передать его в Paginator,
        # для нахождения страницы
        page = request.GET.get('page')
        try:
            # Если существует, то выбираем эту страницу
            context['article_lists'] = current_page.page(page)
        except PageNotAnInteger:
            # Если None, то выбираем первую страницу
            context['article_lists'] = current_page.page(1)
        except EmptyPage:
            # Если вышли за последнюю страницу, то возвращаем последнюю
            context['article_lists'] = current_page.page(current_page.num_pages)

        return render_to_response('home/index.html', context)


# For Error 403 404 500
from django.shortcuts import render_to_response

from django.template import RequestContext

# For RSS feed
"""
class ArticlesFeed(Feed):
    title = "EVILEG - Practic programmers"
    description = "Last article site EVILEG about programmers and IT"
    link = "/"
 
    def items(self):
        return Article.objects.exclude(article_status=False).order_by('-article_date')[:10]
 
    def item_title(self, item):
        return item.article_title
 
    def item_description(self, item):
        return item.article_content[0:400] + "<p>Article first be on - Practic programmers</p>"
"""
# For Error 403 404 500
def e_handler404(request):
    context = RequestContext(request)
    response = render_to_response('home/error404.html', context = context)
    response.status_code = 404
    return response

def e_handler500(request):
    response = render_to_response('home/error500.html', {'request':request}, RequestContext(request))
    response.status_code = 500
    return response 

def csrf_failure(request, reason=""):
    context = RequestContext(request)
    response = render_to_response('home/error403.html', context = context)
    response.status_code = 403
    return response