# -*- coding: utf-8 -*-

from django.views import View
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib import auth
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf

from blog.models import Article
from post.models import Comment
from post.forms import CommentForm


class EArticleView(View):
    template_name = 'post/article.html'
    comment_form = CommentForm

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=self.kwargs['article_id'])
        context = {}
        context.update(csrf(request))
        user = auth.get_user(request)
	context['article'] = article
        context['comments'] = article.comment_set.all().order_by('path')
        context['next'] = article.get_absolute_url()
        if user.is_authenticated:
	        context['form'] = self.comment_form

        return render_to_response(template_name=self.template_name, context=context)


@login_required
@require_http_methods(["POST"])

def add_Comment(request, article_id):
    form = CommentForm(request.POST)
    article = get_object_or_404(Article, id=article_id)
    if form.is_valid():
        comment = Comment()
        comment.path = []
        comment.article_id = article
        comment.author_id = auth.get_user(request)
        comment.content = form.cleaned_data['comment_area']
        comment.save()
	try:
            comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
            comment.path.append(comment.id)
        except ObjectDoesNotExist:
            comment.path.append(comment.id)
        comment.save()

    return redirect(article.get_absolute_url())
