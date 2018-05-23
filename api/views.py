from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.permissions import IsOwnerOrReadOnly
from api.serializers import ProductSerializer, UserSerializer, CatalogSerializer
from mainstore.models import Catalog, Product


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('api:user-list', request=request, format=format),
        'catalogs': reverse('api:catalog-list', request=request, format=format),
        'products': reverse('api:product-list', request=request, format=format)
    })


class CatalogList(generics.ListCreateAPIView):
    """
    get:List all of catalogs
    post:create a new catalog
    """
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    # need ,
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class CatalogDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve:Return a catalog instance.
    update:Return updated catalog
    Destroy:Delete a catalog
    """
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProductList(generics.ListCreateAPIView):
    """
    get:List all of products
    post:create a new product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # need ,
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
     retrieve:Return a user instance.
     update:Return a updated product
     delete:Delete a product by owner only
     """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserList(generics.ListAPIView):
    """
    get:List all of users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserDetail(generics.RetrieveAPIView):
    """
    retrieve:Return a user instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class ProductList1(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # renderer_classes=renderers.JSONRenderer
    # need ,
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(Product.name)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
