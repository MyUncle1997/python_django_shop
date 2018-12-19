from django.conf.urls import url
from . import views
urlpatterns = [
    #个人用户支付
    url(r'^play/',views.play,name='play' ),
    url(r'^playhan/',views.playhan,name='playhan' ),
    url(r'^payorder/',views.payorder,name='payorder' ),
    url(r'^pay_continue/(?P<pk>[0-9]+)?',views.pay_continue,name='pay_continue' ),
    #购物车下单支付
    url(r'^play_shopping/',views.play_shopping,name='play_shopping' ),
    #支付成功
    url(r'^play_success/',views.play_success,name='play_success' ),
    url(r'^play_success_one/',views.play_success_one,name='play_success_one' ),
]