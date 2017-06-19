# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import View
from django.shortcuts import render_to_response, get_object_or_404
from tools import get_client_ip, get_next_url

from django.db.models import Sum

from django.utils import timezone

from .models import *


class EKnowledgeIndex(View):
    template_name = 'blog/index.html'
 
    def get(self, request, *args, **kwargs):
        context = {}
        context['section_list'] = Section.objects.all().order_by('section_title')
        context['ip_addr']=get_client_ip(self.request)
        context['next_url'] = get_next_url(self.request)
 
        return render_to_response(template_name=self.template_name, context=context)
 
 
class ESectionView(View):
    template_name = 'blog/section.html'
 
    def get(self, request, *args, **kwargs):
        context = {}
        section = get_object_or_404(Section, section_url=self.kwargs['section'])
        
        context['section'] = section
 
        return render_to_response(template_name=self.template_name, context=context)
 
 
class EArticleView(View):
    template_name = 'blog/article.html'
 
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=self.kwargs['article_id'])
        context = {}
        context['article'] = article

        obj,created = ArticleStatistic.objects.get_or_create(
            defaults = {
                "article":article,
                "date":timezone.now()
            },
            date = timezone.now(), article = article
        )
        obj.views+=1
        obj.save(update_fields = ['views'])

        popular = ArticleStatistic.objects.filter(
            date__range = [timezone.now() - timezone.timedelta(7), timezone.now()]
        ).values(
            'article_id', 'article__article_title'
        ).annotate(
            views=Sum('views')
        ).order_by(
            '-views')[:5]

        context['popular_list'] = popular

        return render_to_response(template_name=self.template_name, context=context)

