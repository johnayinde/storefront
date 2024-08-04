from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from .models import Customer, Order, OrderItem, Product,Collection, Promotion
# Register your models here.


class InventoryCustomFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = 'inventory'
    
    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<10','Low')
        ]
        
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt = 10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection','promotions']
    search_fields =['title']
    prepopulated_fields ={
        'slug':['title']
    }
    actions =[ 'clear_inventory']
    list_display = ['id','title', 'unit_price','inventory','inventory_status','collection_title',]
    list_editable = ['unit_price','inventory']
    list_per_page = 30
    list_select_related= ['collection']
    list_filter = ['collection','last_update',InventoryCustomFilter]
    
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'OK' 
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self,request, queryset):
        updated = queryset.update(inventory=0)
        self.message_user(request,f'{updated} products were successfully updated')
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership', 'order_count']
    list_editable=['membership']
    ordering = ['first_name','last_name']
    list_per_page = 10 
    search_fields = ['first_name__istartswith','last_name__istartswith']
    
    def order_count(self,customer):
        url = (
            reverse('admin:store_order_changelist') 
            + '?' 
            + urlencode({
                'customer__id': str(customer.id)
        }))
        return format_html('<a href="{}">{}</a>',url,customer.order_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            order_count=Count('order')
        )
    
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields =['product']
    extra= 0
    # min_num =1
    max_num=10
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemInline]
    list_display = ['id','placed_at', 'customer']
    autocomplete_fields =['customer']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','product_count']
    list_select_related=['featured_product']
    search_fields =['title']
    
    @admin.display(ordering='product_count')
    def product_count(self,collection): 
        url = (
            reverse('admin:store_product_changelist') 
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} products</a>',url,collection.product_count)
         
    
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )
        
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    search_fields =['discount']