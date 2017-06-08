# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import View
from django.shortcuts import render_to_response, get_object_or_404

from .models import *


class EKnowledgeIndex(View):
    template_name = 'blog/index.html'
 
    def get(self, request, *args, **kwargs):
        context = {}
        context['section_list'] = Section.objects.all().order_by('section_title')
 
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
        context = {}
        article = get_object_or_404(Article, id=self.kwargs['article_id'])
        
        context['article'] = article
 
        return render_to_response(template_name=self.template_name, context=context)