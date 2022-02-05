from django.db import models
from django.forms import CharField

# Model for a post that goes in user's notes field with image and text translated from image
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=2000, blank = True)
    image = models.ImageField(upload_to="images")

# Model for a user with username and notes fields
class Person(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, blank=True)
    notes = models.ManyToManyField(Post, symmetrical=False, blank=True)
