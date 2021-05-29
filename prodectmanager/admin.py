from django.contrib import admin

# Register your models here.
from .models import Prodects, Category, Subcategory



admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Prodects)
