from django.contrib import admin
from .models import *

admin.site.register(
    [Category, SubCategory, Seller, Product, Media, Ad, Property, Variant, Choice, Review]
)
