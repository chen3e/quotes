from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.main),
    url(r'^/create$', views.create),
    url(r'^/(?P<user_id>\d+)$', views.show_user),
    url(r'^/like/(?P<user_id>\d+)/(?P<quote_id>\d+)$', views.like),
    url(r'^/unlike/(?P<user_id>\d+)/(?P<quote_id>\d+)$', views.unlike),
    url(r'^/delete/(?P<quote_id>\d+)$', views.delete_quote),
]