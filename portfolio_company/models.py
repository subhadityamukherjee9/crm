from django.db import models
from django.contrib import admin

class Founders(models.Model):
    founder_name=models.CharField(max_length=100)
    profile=models.URLField(blank=True,null=True)
    linkedin_url=models.URLField(blank=True,null=True)
    founder_image= models.ImageField(upload_to="founder", null=True, blank=True)


# Create your models here.
class PortfolioCompany(models.Model):
    company_name = models.CharField(default="", blank=True, null=True, max_length=200)
    company_subhead = models.CharField(default="", blank=True, null=True, max_length=300)
    description = models.TextField(blank=True, null=True)
    show_on_profile = models.BooleanField(default=False)
    portfolio_company_link = models.URLField(null=True, blank=True)
    priority = models.IntegerField(default=0, max_length=10)
    portfolio_image = models.ImageField(upload_to="logo", null=True, blank=True)
    portfolio_background_image = models.ImageField(upload_to="background", null=True, blank=True)
    founders = models.ManyToManyField(Founders, blank=True, null=True)
    company_logo = models.ImageField(upload_to="logo", null=True, blank=True)
    short_description= models.TextField(blank=True, null=True)

admin.site.register(PortfolioCompany)
admin.site.register(Founders)

