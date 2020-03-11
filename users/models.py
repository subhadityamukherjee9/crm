from django.db import models
from django.shortcuts import render

class CustomUser(models.Model):
	cho =(('Client', 'Client'),('Employee', 'Employee'))
	user = models.OneToOneField("auth.User")
	types=models.CharField(max_length=10,choices=cho)
	
	def save(self,force_insert=False,*args, **kwargs):
		if self.types=='Employee':
			self.user.is_superuser=True
			self.user.is_staff=True
			self.user.save(*args,**kwargs)
				
		else:
			self.user.is_superuser=False
			self.user.is_staff=False
			self.user.save(*args,**kwargs)
			

				
 	
























	