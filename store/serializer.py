from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection


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
                  'description', 'price_with_tax', 'collection']

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
