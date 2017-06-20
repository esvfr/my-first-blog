# -*- coding: utf-8 -*-

from django import template
from django.db.models import Sum
from django.utils import timezone

from blog.models import ArticleStatistic

register = template.Library()


@register.simple_tag
def get_popular_articles_for_week():

    popular = ArticleStatistic.objects.filter(
        date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]
    ).values(
        'article_id', 'article__article_title', 'views',
    ).annotate(
        sum_views=Sum('views')
    ).order_by(
        '-sum_views')[:5]

    return popular