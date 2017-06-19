from django.contrib import admin
from .models import Section, Article, ArticleStatistic, ArticleStatisticAdmin

admin.site.register(Section)
admin.site.register(Article)
admin.site.register(ArticleStatistic, ArticleStatisticAdmin)
