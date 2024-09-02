from urllib.request import Request
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Count
from store.models import Product, Collection
from store.serializer import CollectionSerializer, ProductSerializer


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()[:5]
    serializer_class = ProductSerializer

    # Over ride the below methods
    # def get(self, request):
    #     q_set = Product.objects.select_re lated('collection').all()[:5]
    #     serialized_products = ProductSerializer(
    #         q_set, many=True, context={'request': request}).data
    #     return Response(serialized_products)

    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     print(serializer.validated_data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serialized_data = ProductSerializer(product).data
    #     return Response(serialized_data)

   # override the delete mixin
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': "Product cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('product')).all()[:5]
    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('product'))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        print(collection.product_set)
        print(collection.product_set.count())
        if collection.product_set.count() > 0:
            return Response({'error': "Collection cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PATCH', 'DELETE'])
# def collection_detail(request, id):
#     collection = get_object_or_404(Collection.objects.annotate(
#         products_count=Count('product')), pk=id)
#     if request.method == "GET":
#         serialized_data = CollectionSerializer(collection).data
#         return Response(serialized_data)
