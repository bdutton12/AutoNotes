from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Person

admin.site.register(Post)
admin.site.register(Person)