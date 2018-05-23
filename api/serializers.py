from django.contrib.auth.models import User
from rest_framework import serializers

from mainstore.models import Catalog, Product


# hyperlinkedmodelserializer
#view_name='api:product-detail'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:user-detail')
    products = serializers.HyperlinkedRelatedField(many=True, view_name='api:product-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'products')


class CatalogSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many=True, view_name='api:product-detail', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='api:catalog-detail')

    class Meta:
        model = Catalog
        fields = ('url', 'id', 'name', 'slug', 'products')
        # look


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:product-detail')
    catalog_id = serializers.HyperlinkedRelatedField(queryset=Catalog.objects.all(), view_name='api:catalog-detail',
                                                     read_only=False)
    catalog = serializers.HyperlinkedRelatedField(view_name='api:catalog-detail', read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = (
            'url', 'id', 'name', 'price', 'slug', 'catalog_id', 'catalog', 'quantity', 'available', 'is_new', 'color',
            'size',
            'owner')


    def create(self, validated_data):
        """
        Create and return a new 'Product' instance, given the validated data.
        """
        # get id only

        catalog_id = validated_data.pop('catalog_id').id
        print('ccccc id is :', catalog_id)

        # if 'catalog' in validated_data.keys():
        #     catalog_data = validated_data.pop('catalog')
        #     print("catalog_id :",catalog_id)
        #     catalog=CatalogSerializer.create(CatalogSerializer(),validated_data=catalog_data)
        #
        #     product=Product.objects.create(catalog=catalog,catalog_id=catalog_id,**validated_data)
        # else:
        product = Product.objects.create(catalog_id=catalog_id, **validated_data)
        return product

    def update(self, instance, validated_data):
        """
        Update and return an existing 'Product' instance, given the validated data
        """
        try:
            catalog_id=validated_data.pop('catalog_id').id
        except catalog_id.DoesNotExit:
            raise
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.color = validated_data.get('color', instance.color)
        instance.size = validated_data.get('size', instance.size)
        instance.available = validated_data.get('available', instance.available)
        instance.is_new = validated_data.get('is_new', instance.is_new)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.catalog_id = validated_data.get('catalog_id', instance.catalog_id)

        if str(catalog_id):
            pass
            # catalog=Catalog.objects.get(pk=catalog_id)
            # print("catalog for updating:",catalog)
            # catalog.url=catalog.get('url',catalog)
            # catalog.save()
        instance.save()
        return instance
