from django.contrib import admin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TagItem
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.


class TagInline(GenericTabularInline):
    model = TagItem
    extra = 0
    min_num = 1
    autocomplete_fields = ['tag']
    
class CustomProductAdmin(ProductAdmin):
    inlines=[TagInline]
    
admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)