# Create your tests here.
import json

from decimal import Decimal
from django.contrib.auth.models import User
from django.core import serializers
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from mainstore.models import Catalog, Product


class BasesetUptearDown(APITestCase):
    def setUp(self):
        print("\n*****************time:{}****************".format(now()))
        print("\n************setUp*******************")
        self.client = APIClient()
        # create test user
        self.user = User.objects.create_superuser(username='miketheknighttester', email='miketheknighttester@test.com',
                                                  password='abctest123')
        self.client.login(username='miketheknighttester', password='abctest123')

        # setUp for catalog
        self.request_data = {
            "name": "catalogtestcase4",
            "slug": "catalog-testcase-4"
        }

        self.catalog = Catalog.objects.create(name='catalogtestcase5', slug='catalog-testcase-5-1')
        print("catalog id:", self.catalog.id)
        print("catalog name:", self.catalog.name)
        print("catalog slug:", self.catalog.slug)

        # setUp for product
        # self.request_data_product = {
        #     "name": "tt",
        #     "price": 21.55,
        #     "slug": "tt",
        #     "catalog_id": 1,
        #     "quantity": 2,
        #     "available": True,
        #     "is_new": False,
        #     "color": "white",
        #     "size": "one size"
        # }
        # "http://127.0.0.1:8000/api/catalogs/1/"
        self.request_data_product = {
            "name": "tt1",
            "price": "350.99",
            "slug": "tt1",
            "catalog_id": "http://127.0.0.1:8000/api/catalogs/1/",
            "quantity": 22,
            "available": True,
            "is_new": True,
            "color": "black",
            "size": "5.1"
        }
        # self.request_data_product = json.dumps(data_product)

        self.product=Product.objects.create(name='tt2',
                                            price='350.99',
                                            slug='tt2',
                                            catalog_id=1,
                                            quantity='22',
                                            available='0',
                                            is_new='0',
                                            color="black",
                                            size="5.1")
        # self.product = Product.objects.create(self.request_data_product)
        print("product setUp: ", self.product)

    def tearDown(self):
        print("\n***************************tearDown*************************************")


# Catalog TestCases

class CatalogListTestCase(APITestCase):
    url_reverse = reverse('api:catalog-list')
    url = '/api/catalogs/'

    # url_detail='/api/catalogs/{}/'

    def setUp(self):
        BasesetUptearDown.setUp(self)

    # slug is unique
    def test_api_catalog_create(self):

        print("\n************" + self._testMethodName + "*******************")
        print("url and data:{}-{}".format(self.url, self.request_data))
        print("user is:", self.user)

        self.response = self.client.post(self.url, self.request_data, format='json')
        print("self-response:", self.response)

        self.assertEqual(Catalog.objects.count(), 2)
        print("id is :", self.catalog.id)
        if self.catalog:
            new_id = self.catalog.id + 1
        else:
            new_id = self.catalog.id
        print("new id is:", new_id)
        self.assertEqual(Catalog.objects.get(pk=new_id).name, self.request_data.get('name'))
        self.assertEqual(Catalog.objects.get(pk=new_id).slug, self.request_data.get('slug'))
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        BasesetUptearDown.tearDown(self)


#
class CatalogDetailTestCase(APITestCase):
    url_detail_reverse = reverse('api:catalog-detail', kwargs={"pk": 1})
    url_detail = '/api/catalogs/{}/'

    def setUp(self):
        BasesetUptearDown.setUp(self)

    def test_api_catalog_update(self):
        print("\n************" + self._testMethodName + "*******************")
        print("before update catalog:", self.catalog.slug)

        # name and slug are not null

        update_data = {
            "name": "catalogtestcase5-update",
            "slug": "catalog-testcase-5-3"
        }
        print('url is :{}'.format(self.url_detail.format(self.catalog.id)))
        response = self.client.put(self.url_detail.format(self.catalog.id), update_data, format='json')

        print('c id is:', self.catalog.id)
        db_slug = Catalog.objects.get(pk=self.catalog.id).slug
        self.assertEqual(db_slug, update_data.get('slug'))
        print("after update catalog:", db_slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_api_catalog_partial_update(self):
        print("\n************" + self._testMethodName + "*******************")
        print("before partial update catalog:", self.catalog.slug)

        # name and slug are not null
        name = self.catalog.name
        update_data = {
            "name": name,
            "slug": "catalog-testcase-5-3"
        }
        print('url is :{}'.format(self.url_detail.format(self.catalog.id), ))
        response = self.client.put(self.url_detail.format(self.catalog.id), update_data, format='json')

        print('c id is:', self.catalog.id)
        db_slug = Catalog.objects.get(pk=self.catalog.id).slug
        self.assertEqual(db_slug, update_data.get('slug'))
        print("after partial update catalog:", db_slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_api_catalog_retrieve(self):
        print("\n************" + self._testMethodName + "*******************")
        db_catalog = Catalog.objects.get(pk=self.catalog.id)
        response = self.client.get(self.url_detail.format(self.catalog.id), format='json')
        self.assertEqual(response.data.get('name', None), db_catalog.name)
        self.assertEqual(response.data.get('slug', None), db_catalog.slug)
        print("response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_api_catalog_delete(self):
        print("\n************" + self._testMethodName + "*******************")
        print("---id is:", self.catalog.id)
        print("---name is:", self.catalog.name)
        response = self.client.delete(self.url_detail.format(self.catalog.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        BasesetUptearDown.tearDown(self)


# product TestCases

class ProductListTestCase(APITestCase):
    url_reverse = reverse('api:product-list')
    url = '/api/products/'

    # url_detail='/api/products/{}/'

    def setUp(self):
        BasesetUptearDown.setUp(self)


    def test_api_product_create(self):

        print("\n************" + self._testMethodName + "*******************")
        print("url and data:\n {}-{}".format(self.url, self.request_data_product))
        print("user is:", self.user)

        self.response = self.client.post(self.url, self.request_data_product, format='json')
        print("self-response:", self.response)
        self.assertEqual(Product.objects.count(), 2)
        # self.assertEqual(product.objects.get(pk=self.product.id).name, 'producttestcase1')
        print("id is :", self.product.id)
        if self.product:
            new_id = self.product.id + 1
        else:
            new_id = self.product.id
        print("product new id is:", new_id)
        self.assertEqual(Product.objects.get(pk=new_id).name, self.request_data_product.get('name'))
        self.assertEqual(Product.objects.get(pk=new_id).slug, self.request_data_product.get('slug'))
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


    def tearDown(self):
        BasesetUptearDown.tearDown(self)


class ProductDetailTestCase(APITestCase):
    url_detail_reverse = reverse('api:product-detail', kwargs={"pk": 1})
    url_detail = '/api/products/{}/'

    def setUp(self):
        BasesetUptearDown.setUp(self)

    def test_api_product_update(self):
        print("\n************" + self._testMethodName + "*******************")
        print("before update product:", self.product.slug)
        print("COUNT: ",Product.objects.count())

        # name and slug are not null

        update_data = {
            "name": "tt55",
            "price": "351.99",
            "slug": "tt55",
            "catalog_id": "http://127.0.0.1:8000/api/catalogs/1/",
            "quantity": 20,
            "available": False,
            "is_new": True,
            "color": "white",
            "size": "5.5"
        }
        print('url is :{}'.format(self.url_detail.format(self.product.id)))
        response = self.client.put(self.url_detail.format(self.product.id), update_data, format='json')
        print("Response data after put:",response.data)

        print('p id is:', self.product.id)
        db_slug = Product.objects.get(pk=self.product.id).slug
        print("after update product:", db_slug)
        self.assertEqual(db_slug, update_data.get('slug'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_api_product_partial_update(self):
        print("\n************" + self._testMethodName + "*******************")
        print("before partial update product:", self.product.slug)

        # name and slug are not null
        update_data = {
            # "name": "tt56",
            # "price": "350.99",
            "slug": "tt58",
            "catalog_id": "http://127.0.0.1:8000/api/catalogs/1/",
            "quantity": 22
        }
        print('url is :{}'.format(self.url_detail.format(self.product.id), ))
        # response = self.client.put(self.url_detail.format(self.product.id), update_data, format='json')
        response=self.client.patch(self.url_detail.format(self.product.id), update_data, format='json')
        print("Response data after patch:", response.data)

        print('p id is:', self.product.id)
        db_slug = Product.objects.get(pk=self.product.id).slug
        self.assertEqual(db_slug, update_data.get('slug'))
        print("after partial update product:", db_slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_product_retrieve(self):
        print("\n************" + self._testMethodName + "*******************")
        db_product = Product.objects.get(pk=self.product.id)
        response = self.client.get(self.url_detail.format(self.product.id), format='json')
        self.assertEqual(response.data.get('name', None), db_product.name)
        self.assertEqual(response.data.get('slug', None), db_product.slug)
        self.assertEqual(Decimal(response.data.get('price', None)), db_product.price)
        print("response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #
    def test_api_product_delete(self):
        print("\n************" + self._testMethodName + "*******************")
        print("---id is:", self.product.id)
        print("---name is:", self.product.name)
        response = self.client.delete(self.url_detail.format(self.product.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        BasesetUptearDown.tearDown(self)
