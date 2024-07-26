from django.db import models

# Create your models here.

class Collection(models.Model):
    title = models.CharField( max_length=50)
    featured_product = models.ForeignKey("Product",  on_delete=models.SET_NULL, null=True,related_name='+')
    
class Promotion(models.Model):
    description = models.TextField()
    discount= models.FloatField()
    
class Product(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SLIVER='S'
    MEMBERSHIP_GOLD='G'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SLIVER,'Sliver'),
        (MEMBERSHIP_GOLD,'Gold'),
    ]
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6 , decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True )
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion )
    
    
    
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)   
     
     class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
     
    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_COMPLETE,'Complete'),
        (PAYMENT_STATUS_FAILED,'FAILED'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_METHOD_CHOICES,default=PAYMENT_STATUS_PENDING )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,  on_delete=models.PROTECT)
    product = models.ForeignKey(Product,  on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField( max_digits=6, decimal_places=2)
    
class Address(models.Model):
        street = models.CharField(max_length=255)
        city = models.CharField(max_length=255)
        customer = models.OneToOneField(Customer, primary_key=True, on_delete=models.CASCADE)
        

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()