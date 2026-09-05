from django.contrib import admin
from .models import Category

# Register your Category model so it shows up in the admin dashboard
admin.site.register(Category)
