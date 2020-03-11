from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
import os
from datetime import datetime
from multiselectfield import MultiSelectField
#from shortuuidfield import ShortUUIDField
def get_image_path(user, filename, max_length=None):
    _datetime = datetime.now()
    datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
    # if there are more than one dots
    file_name_split = filename.split('.')
    file_name_list = file_name_split[:-1]
    ext = file_name_split[-1]
    file_name_wo_ext = '.'.join(file_name_list)
    name = '{0}-{1}.{2}'.format(file_name_wo_ext, datetime_str, ext)
    return os.path.join('photos', name)

class Contacts(models.Model):
    cho =(('Angel', 'Angel'),('Expert', 'Expert'),('GP', 'GP'),('LP', 'LP'))

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=250)
    title = models.CharField(max_length=500)
    email = models.EmailField()
    role = MultiSelectField(max_length=100,choices=cho)
    past_investment = models.CharField(max_length=100, blank=True, null=True)
    img_file = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    img_url=models.URLField(null=True,blank=True)
    linkedin_url=models.URLField(null=True,blank=True)
    connection = models.ManyToManyField(User,blank=True,null=True)
    company = models.ManyToManyField("pcontact.CompanyAssociation")
    institute = models.ManyToManyField("pcontact.InsttitueAssociation")
    tags = models.ManyToManyField("pcontact.Tags",blank=True)
    class Meta:
        verbose_name_plural = "Contacts"
    def __str__(self):
        return "%s" % (self.name)


class Company(models.Model):
    company_name = models.TextField(max_length=200)
    location=models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        verbose_name_plural = "Company"
    def __str__(self):
        return "%s" % (self.company_name)

class Institute(models.Model):
    institute_name = models.TextField(max_length=200)
    location=models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        verbose_name_plural = "Institute"
    def __str__(self):
        return "%s" % (self.institute_name)

class Tags(models.Model):
    tag_name=models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        verbose_name_plural = "Tags"
    def __str__(self):
        return "%s" % (self.tag_name)

class CompanyAssociation(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True,blank=True)
    year=models.CharField(max_length=30, null=True,blank=True)
    location=models.CharField(max_length=200, null=True,blank=True)
    class Meta:
        verbose_name_plural = "Company Association"
    def __str__(self):
        return "%s" % (self.company)


class InsttitueAssociation(models.Model):
    institute=models.ForeignKey(Institute,on_delete=models.CASCADE)
    year=models.CharField(max_length=30,null=True,blank=True)
    degree=models.CharField(max_length=200,default='')
    class Meta:
        verbose_name_plural = "Institute Association"
    def __str__(self):
        return "%s" % (self.institute)
