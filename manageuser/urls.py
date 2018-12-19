from django.conf.urls import url
from . import views
from .import Code
urlpatterns = [
    #卖家选择
    url(r'^manage_shop_home/', views.manage_shop_home, name='manage_shop_home'),
    #登录路由
    url(r'^manage_login/',views.manage_login,name='manage_login'),
    url(r'^manage_login_han/',views.manage_login_han,name='manage_login_han'),
    url(r'^manage_home/(?P<pk>[0-9]+)?',views.manage_home,name='manage_home'),
    url(r'^manage_login_out/',views.manage_login_out,name='manage_login_out'),
    url(r'^manage_Code',Code.tu),
    #商品路由
    url(r'^manage_add/',views.manage_add,name='manage_add'),
    url(r'^manage_add_han/',views.manage_add_han,name='manage_add_han'),
    url(r'^manage_add_list/', views.manage_add_list, name='manage_add_list'),
    url(r'^manage_add_list_del/(?P<pk>[0-9]+)?', views.manage_add_list_del, name='manage_add_list_del'),
    url(r'^manage_add_list_modify/(?P<pk>[0-9]+)?', views.manage_add_list_modify, name='manage_add_list_modify'),
    url(r'^manage_add_modify_han/', views.manage_modify_han, name='manage_modify_han'),
    #商品上架/下架
    url(r'^manage_add_up/(?P<pk>[0-9]+)?',views.manage_add_up, name='manage_add_up'),
    url(r'^manage_add_dowm/(?P<pk>[0-9]+)?',views.manage_add_dowm, name='manage_add_dowm'),
    #类别路由
    url(r'^manage_leibie/',views.manage_leibie,name='manage_leibie'),
    url(r'^manage_leibie_han/',views.manage_leibie_han,name='manage_leibie_han'),
    url(r'^manage_leibie_del/(?P<pk>[0-9]+)?',views.manage_leibie_del,name='manage_leibie_del'),
    url(r'^leibie_modify/(?P<pk>[0-9]+)?',views.leibie_modify,name='leibie_modify'),
    url(r'^leibie_modify_han/',views.leibie_modify_han,name='leibie_modify_han'),
    url(r'^manage_leibie_list/', views.manage_leibie_list, name='manage_leibie_list'),
    #商家订单管理
    url(r'^manage_order_list/', views.manage_order_list, name='manage_order_list'),
    url(r'^manage_order_page/(?P<pk>[0-9]+)?', views.manage_order_page, name='manage_order_page'),
    url(r'^manage_order_comment/(?P<pk>[0-9]+)?', views.manage_order_comment, name='manage_order_comment'),
    #发货操作
    url(r'^manage_logistics/(?P<pk>[0-9]+)?', views.manage_logistics, name='manage_logistics'),
    url(r'^manage_logistics_han/', views.manage_logistics_han, name='manage_logistics_han'),
    #会员管理
    url(r'^manage_member_list/', views.manage_member_list, name='manage_member_list'),
    url(r'^manage_member_email/(?P<pk>[0-9]+)?', views.manage_member_email, name='manage_member_email'),
    url(r'^manage_show_email/(?P<pk>[0-9]+)?', views.manage_show_email, name='manage_show_email'),
    url(r'^manage_member_han/', views.manage_member_han, name='manage_member_han'),
    #权限管理
    url(r'^manage_power_list/', views.manage_power_list, name='manage_power_list'),
    url(r'^manage_power_add/', views.manage_power_add, name='manage_power_add'),
    url(r'^manage_power_han/', views.manage_power_han, name='manage_power_han'),
    url(r'^manage_power_modify/(?P<pk>[0-9]+)', views.manage_power_modify, name='manage_power_modify'),
    url(r'^manage_power_modify_han/', views.manage_power_modify_han, name='manage_power_modify_han'),
    url(r'^manage_power_del/', views.manage_power_del, name='manage_power_del'),
    #角色管理
    url(r'^manage_role_list/', views.manage_role_list, name='manage_role_list'),
    url(r'^manage_role_add/', views.manage_role_add, name='manage_role_add'),
    url(r'^manage_role_modify/', views.manage_role_modify, name='manage_role_modify'),
    url(r'^manage_role_del/', views.manage_role_del, name='manage_role_del'),
]