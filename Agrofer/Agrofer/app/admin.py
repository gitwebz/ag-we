from django.contrib import admin
from .models import Product, BlogPost, ContactSubmission

# Register your models
admin.site.register(Product)
admin.site.register(BlogPost)
admin.site.register(ContactSubmission)