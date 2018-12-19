from django.conf.urls import url
from . import views
urlpatterns = [
    #订单处理
    url(r'^order/',views.order,name='order' ),
    url(r'^order_dowm/',views.order_dowm,name='order_dowm' ),
    url(r'^order_han/',views.order_han,name='order_han' ),
    url(r'^order_save/',views.order_save,name='order_save' ),
    url(r'^order_success/',views.order_success,name='order_success' ),
    #地址管理
    url(r'^order_address/',views.order_address,name='order_address' ),
    url(r'^order_address_han/',views.order_address_han,name='order_address_han' ),
    #用户下单
    url(r'^order_dowm_user/',views.order_dowm_user,name='order_dowm_user' ),
    url(r'^order_dowm_user_han/',views.order_dowm_user_han,name='order_dowm_user_han' ),
    url(r'^order_user_success/',views.order_user_success,name='order_order_user_success' ),
    #勾选下单
    url(r'^order_check/',views.order_check,name='order_check' ),
]