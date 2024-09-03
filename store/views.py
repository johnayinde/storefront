from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from store.models import OrderItem, Product, Collection
from store.serializer import CollectionSerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': "Product cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     if product.orderitems.count() > 0:
    #         return Response({'error': "Product cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
    #     product = get_object_or_404(Product, pk=pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('product')).all()[:5]
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': "Collection cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
