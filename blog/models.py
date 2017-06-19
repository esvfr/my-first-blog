from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

"""
class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()
	def __str__(self):
		 return self.title
"""


class Section(models.Model):
    class Meta:
        db_table = "section"

    section_title = models.CharField(max_length=200)
    section_url = models.CharField(max_length=50)
    section_description = models.TextField()

    def __str__(self):
        return self.section_title


class Article(models.Model):
    class Meta:
        db_table = "article"

    article_title = models.CharField('Name article', max_length=200)
    article_section = models.ForeignKey(Section)
    article_author = models.ForeignKey(User)
    article_date = models.DateTimeField('Date published')
    article_content = models.TextField()
    article_status = models.IntegerField()

    def __str__(self):
        return self.article_title


class ArticleStatistic(models.Model):
    class Meta:
        db_table = "ArticleStatistic"

    article = models.ForeignKey(Article)  # external key on article
    date = models.DateField('Date', default=timezone.now)  # Date
    views = models.IntegerField('Views', default=0)  # quantity views of this date

    def __str__(self):
        return self.article.article_title


class ArticleStatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'views')  # views fields in admin
    search_fields = ('__str__',)  # field for search

# For RSS


def get_absolute_url(self):
    return reverse('blog:article', kwargs={'section': self.article_section.section_url,
                                           'article_id': self.id})
