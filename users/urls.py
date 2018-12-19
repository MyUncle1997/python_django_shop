from django.conf.urls import url
from . import views
from . import Code
urlpatterns = [
    #用户注册
    url(r'^register/',views.register,name='register' ),
    url(r'^register_handel/',views.register_handel,name='register_handel' ),
    #用户登录
    url(r'^login/', views.login, name='login'),
    url(r'^login_quit/', views.login_quit, name='login_quit'),
    url(r'^login_handel/', views.login_handel, name='login_handel'),
    url(r'^Code/',Code.huitu, ),
    #用户后台
    url(r'^user_order/', views.user_order, name='user_order'),
    url(r'^user_order_confirm/(?P<pk>[0-9]+)?', views.user_order_confirm, name='user_order_confirm'),
    url(r'^user_modify/', views.user_modify, name='user_modify'),
    url(r'^user_address/', views.user_address, name='user_address'),
    url(r'^user_order_pg/(?P<pk>[0-9]+)?', views.user_order_pg, name='user_order_pg'),
    url(r'^user_order_logistics/(?P<pk>[0-9]+)?', views.user_order_logistics, name='user_order_logistics'),
    #用户修改
    url(r'^user_modify_han/', views.user_modify_han, name='user_modify_han'),
    url(r'^user_address_modify/(?P<pk>[0-9]+)?', views.user_address_modify, name='user_address_modify'),
    url(r'^user_address_del/(?P<pk>[0-9]+)?', views.user_address_del, name='user_address_del'),
    url(r'^user_address_modify_han/', views.user_address_modify_han, name='user_address_modify_han'),
    url(r'^user_address_add/', views.user_address_add, name='user_address_add'),
    url(r'^user_address_add_han/', views.user_address_add_han, name='user_address_add_han'),
    #用户个人信息
    url(r'^user_core/', views.user_core, name='user_core'),
    url(r'^user_core_modify/', views.user_core_modify, name='user_core_modify'),
    url(r'^user_core_modify_han/', views.user_core_modify_han, name='user_user_core_modify_han'),
    #评论功能
    url(r'^user_comment/(?P<pk>[0-9]+)?', views.user_comment, name='user_comment'),
    url(r'^user_comment_body/(?P<pk>[0-9]+)?', views.user_comment_body, name='user_comment_body'),
    url(r'^user_comment_han/', views.user_comment_han, name='user_comment_han'),
    #邮箱注册激活功能
    url(r'^user_activation/', views.user_activation, name='user_activation'),
    url(r'^user_activation_continue/', views.user_activation_continue, name='user_activation_continue'),
    url(r'^user_activation_han/', views.user_activation_han, name='user_activation_han'),
    url(r'^user_reactivation/', views.user_reactivation, name='user_reactivation'),
    #用户收藏
    url(r'^user_collection/',views.user_colletion, name='user_collection'),
    #用户验证码
    url(r'^user_code/',views.user_code, name='user_code'),
]