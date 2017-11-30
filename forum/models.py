from __future__ import unicode_literals

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateField(auto_now=True)
    author = models.CharField(max_length=50,default="Anonymous")

class Comment(models.Model):
    post = models.ForeignKey('Post',on_delete=models.CASCADE,)
    text = models.TextField()
    date = models.DateField(auto_now=True)
    author = models.CharField(max_length=50,default="Anonymous")


    

