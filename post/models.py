# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from blog.models import Article

# Create your models here.
class Comment(models.Model):
    class Meta:
        db_table = "comments"
 
    path = ArrayField(models.IntegerField())
    article_id = models.ForeignKey(Article)
    author_id = models.ForeignKey(User)
    content = models.TextField('Comment')
    pub_date = models.DateTimeField('Date comment', default=timezone.now)
 
    def __str__(self):
        return self.content[0:200]
 
    def get_offset(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return level
 
    def get_col(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return 12 - level
