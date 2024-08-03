from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q,F
from store.models import Product,Customer,Collection,Order,OrderItem
# Create your views here.



def playground(request):
    # q_set = Product.objects.filter(pk=0).first() # get the first value from the filter qSet
    # q_set = Product.objects.filter(unit_price = 20) # get all products price that are  20
    # q_set = Product.objects.filter(unit_price__gt = 20) # get all products price that are more then 20 
    # q_set = Product.objects.filter(unit_price__range=(20,100)) # get all products price that are between the range (20-100) 
    # q_set = Product.objects.filter(collection__id__range=(3,5)) # get all products in collection id 3 & 5 
    # q_set = Product.objects.filter(title__icontains= "tofu") # get all products whose title contains "" (in-sensitive serch)
    # q_set = Product.objects.filter(description__isnull=True) # get all products description which are null 
    
    ## Execise
    # • Customers with .com accounts 
    customer = Customer.objects.filter(email__icontains='.com') 
    
    # • Collections that don’t have a featured product
    collection = Collection.objects.filter(featured_product_id__isnull=True) 
    # • Products with low inventory (less than 10)
    prod = Product.objects.filter(inventory__lt=10) 
    # • Orders placed by customer with id = 1
    ord = Order.objects.filter(customer_id=1) 
    # • Order items for products in collection 3
    products_in_collection = Product.objects.filter(collection__id=3)
    ord2 = OrderItem.objects.filter(product__in=products_in_collection) 
    for order_item in ord2:
        # print(order_item)
        pass
        
        
    # complex query filters
    
    # product with inventory <10 OR >20
    # inventories = Product.objects.filter(Q(inventory__lt =10) | Q(inventory__gt=20))
    # inventories = Product.objects.filter(Q(inventory__lt =10) | ~Q(inventory__gt=20)) # not >20
    
    # referencing fields 
    # inventories = Product.objects.filter(inventory=F('unit_price')) # where inventory==unit_price 
    
    # prod = Product.objects.values('id','title','unit_price','collection__title')[0:10] # select id,title,price,and related field
    ord2 = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    
    produc = Product()
    produc.t 
    
    return render(request, 'hello.html', {'products': list(ord2)}) 