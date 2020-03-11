from django.db import models
from django.contrib import admin

class CompanyTeam(models.Model):
    team_name= models.CharField(default="", blank=True, null=True, max_length=200)
    team_image= models.ImageField(upload_to="team", null=True, blank=True)
    team_description= models.CharField(default="", blank=True, null=True, max_length=800)
    team_position= models.CharField(default="", blank=True, null=True, max_length=100)
    team_email= models.CharField(default="", blank=True, null=True, max_length=100)
    team_linkedin_url= models.URLField(null=True, blank=True)
    team_twitter_url= models.URLField(null=True, blank=True)

admin.site.register(CompanyTeam)
