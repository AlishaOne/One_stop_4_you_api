from django.conf.urls import url
from django.urls import include
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# be careful its a list [] not { }
# http://127.0.0.1:8000/mainstore/api/
# Add a namespace so Django knows what directory to load
# if another app has views with the same name

app_name = 'api'


# schema_url_patterns = [url(r'^api/', include('api.urls')), ]
# schema_view = get_schema_view(title="Onestop4you API", patterns=schema_url_patterns)
schema_view = get_schema_view(title="Onestop4you API",)
# APPEND_SLASH = False
#r'^catalogs/(?P<pk>[0-9]+)/?$',? means may or may not have /

urlpatterns = [

    url(r'^catalogs/$', views.CatalogList.as_view(), name='catalog-list'),
    url(r'^catalogs/(?P<pk>[0-9]+)/$', views.CatalogDetail.as_view(), name='catalog-detail'),
    url(r'^products/$', views.ProductList.as_view(), name='product-list'),
    url(r'^products/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(), name='product-detail'),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^catalogs/(?P<name>[\w\-?]+)/$', views.CatalogDetail.as_view(), name='catalog-detail'),
    url(r'^$', views.api_root),
    url(r'^schema/$', schema_view),
    # url(r'^/', include(router.urls))

]
urlpatterns = format_suffix_patterns(urlpatterns)
