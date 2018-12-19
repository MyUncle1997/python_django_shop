from django.conf.urls import url
from . import views
urlpatterns = [
    #开店操作
    url(r'^shop_open/',views.shop_open,name='shop_open'),
    url(r'^shop_open_han/', views.shop_open_han, name='shop_open_han'),
    url(r'^shop_add/', views.shop_add, name='shop_add'),
    url(r'^shop_add_han/', views.shop_add_han, name='shop_add_han'),
    #店铺分类
    url(r'^shop_list/', views.shop_list, name='shop_list'),
    url(r'^shop_list_home/(?P<pk>[0-9]+)?', views.shop_list_home, name='shop_list_home'),
    url(r'^shop_home_content/(?P<pk>[0-9]+)/(?P<gk>[0-9]+)?', views.shop_home_content, name='shop_home_content'),
]