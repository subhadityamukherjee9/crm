from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.user_info, name='dashboard'),
    url(r'^lazy_load_posts$', views.lazy_load_posts, name='lazy_load_posts'),
    url(r'^csv/upload/$', views.upload_csv, name='upload'),
    url(r'^email/$',views.email, name='email'),
]
