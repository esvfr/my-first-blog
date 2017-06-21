# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from blog.models import Article

# Create your models here.
class BookmarkBase(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, verbose_name="Пользователь")

    def __str__(self):
        return self.user.username


class BookmarkArticle(BookmarkBase):
    class Meta:
        db_table = "bookmark_article"

    obj = models.ForeignKey(Article, verbose_name="Статья")


"""class BookmarkComment(BookmarkBase):
    class Meta:
        db_table = "bookmark_comment"

    obj = models.ForeignKey(Comment, verbose_name="Комментарий")"""
