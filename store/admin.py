from django.contrib import admin
from store.models import Category,Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields={'slug':('name',)} #bas zid category bas 7ot name la7ala lsulg bttsama metl lname

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields={'slug':('title',)}