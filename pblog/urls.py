from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    #url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^$', views.post_list, name='blog'),
    url(r'^(?P<slug>[-\w]+)/$', views.blog_detail, name='blog-detail'),
    #url(r'^simple_upload/$', views.simple_upload, name='simple_upload'),
]
