from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'slug', 'inventory',
                  'description', 'price_with_tax', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    # # collection = serializers.PrimaryKeyRelatedField(  #show the ID
    # #     queryset=Collection.objects.all()
    # # )
    # collection = CollectionSerializer()

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

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
