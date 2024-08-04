from urllib.request import Request
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from store.models import Product, Collection
from store.serializer import CollectionSerializer, ProductSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        q_set = Product.objects.select_related('collection').all()[:5]
        serialized_products = ProductSerializer(q_set, many=True).data
        return Response(serialized_products)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        serialized_data = ProductSerializer(product).data
        return Response(serialized_data)

    elif request.method == "PATCH":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response({'error': "Product cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request: Request):
    if request.method == 'GET':
        q_set = Collection.objects.annotate(
            products_count=Count('product')).all()[:5]
        serialized_products = CollectionSerializer(q_set, many=True).data
        return Response(serialized_products)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'DELETE'])
def collection_detail(request, id):
    collection = get_object_or_404(Collection.objects.annotate(
        products_count=Count('product')), pk=id)
    if request.method == "GET":
        serialized_data = CollectionSerializer(collection).data
        return Response(serialized_data)

    elif request.method == "PATCH":
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if collection.orderitems.count() > 0:
            return Response({'error': "Collection cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
