from decimal import Decimal
from rest_framework import serializers
from store.models import Cart, Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # # collection = serializers.PrimaryKeyRelatedField(  #show the ID
    # #     queryset=Collection.objects.all()
    # # )
    # collection = CollectionSerializer()         # should nested object of the collection

    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'slug', 'inventory',
                  'description', 'price_with_tax', 'collection', 'last_update']

    # def create(self, validated_data): # override cretion of product
    #     #add new fields to it
    #     product = Product(**validated_data) #unpack the validated data
    #     product.other_field_to_add = "new value"
    #     product.save()
    #     return product

    # def update(self, instance:Product, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description',  'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id']

    # id = serializers.UUIDField(read_only)
    id = serializers.UUIDField(read_only=True)
