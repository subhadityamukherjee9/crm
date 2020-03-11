from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login,  {'template_name': 'login.html'}, name='log-in'),
    url(r'^logout/$', auth_views.logout,{'next_page': '/login'}, name='log-out'),
    url("^fyle/", TemplateView.as_view(template_name="fyle.html"), name='fyle'),
    url("^shubhloans/", TemplateView.as_view(template_name="shubhloans.html"), name='shubhloans'),
    url("^philosophy/", TemplateView.as_view(template_name="philosophy.html"), name='philosophy'),
    url("^team/", views.teams , name='team'),
    url("^portfolio_detail/(?P<portfolio_id>[0-9]+)/$", views.portfolio_detail , name='portfolio_detail'),
    url("^portfolio/", views.portfolio_companies_view, name='portfolio'),
    url("^greyatom/", TemplateView.as_view(template_name="greyatom.html"), name='greyatom'),
    url("^crofarm/", TemplateView.as_view(template_name="crofarm.html"), name='crofarm'),
    url("^ikarus/", TemplateView.as_view(template_name="ikarus.html"), name='ikarus'),
    url("^innovaccer/", TemplateView.as_view(template_name="innovaccer.html"), name='innovaccer'),
    url("^propertyshare/", TemplateView.as_view(template_name="propertyshare.html"), name='propertyshare'),
    url("^workex/", TemplateView.as_view(template_name="workex.html"), name='workex'),
    url("^grubox/", TemplateView.as_view(template_name="grubox.html"), name='grubox'),
    url("^contact-us/", TemplateView.as_view(template_name="contact.html"), name='contact-us'),


    url(r'^forgot-password/$', views.forgotpassword, name='forgotpassword'),
    url(r'^forgot_email/$',views.forgot_email, name='forgot_email'),

    #url(r'^blog/$', views.post_list, name='blog'),
    #url(r'^blog/(?P<slug>[-\w]+)/$', views.blog_details, name='blog-detail'),
    #url(r'^dashboard/$', TemplateView.as_view(template_name="main-page.html"), name='dashboard'),
    #url(r'^simple_upload/$', views.simple_upload, name='simple_upload'),
]
