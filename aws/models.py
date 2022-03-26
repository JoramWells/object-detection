from distutils.command.upload import upload
from django.db import models

# Create your models here.

class Pepper(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
    
class Tomato(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name