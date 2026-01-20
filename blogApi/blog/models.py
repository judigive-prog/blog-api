from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=9000)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.name

