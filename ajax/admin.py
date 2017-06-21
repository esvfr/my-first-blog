# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from ajax.models import BookmarkArticle

admin.site.register(BookmarkArticle)