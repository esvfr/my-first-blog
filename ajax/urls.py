from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ajax.models import BookmarkArticle
from . import views

app_name = 'ajax'
urlpatterns = [
    url(r'^article/(?P<pk>\d+)/bookmark/$',
        login_required(views.BookmarkView.as_view(model=BookmarkArticle)),
        name='article_bookmark'),
]