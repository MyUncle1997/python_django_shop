from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^goods$',views.index,name='goods'),
    url(r'^goods_search$',views.goods_search,name='goods_search'),
]