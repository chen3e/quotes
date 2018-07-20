from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^/(?P<user_id>\d+)$', views.edit),
    url(r'^/edit/(?P<user_id>\d+)$', views.update)
]