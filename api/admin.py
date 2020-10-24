from django.contrib import admin

from .models import Image

# added this for my own dev purposes, not explicitly part of the spec
admin.site.register(Image)