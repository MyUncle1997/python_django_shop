from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^shopping_user/',views.shopping_user,name='shopping_user' ),
    url(r'^shopping_add/',views.shopping_add,name='shopping_add' ),
    url(r'^shopping_del/(?P<pk>[0-9]+)?',views.shopping_del,name='shopping_del' ),
    url(r'^shopping_plus/(?P<pk>[0-9]+)?',views.shopping_plus,name='shopping_plus' ),
    url(r'^shopping_re/(?P<pk>[0-9]+)?',views.shopping_re,name='shopping_re' ),
    url(r'^shopping_w_del/',views.shopping_w_del,name='shopping_w_del' ),
    url(r'shopping_blur/(?P<pk>[0-9]+)?',views.shopping_blur,name='shopping_blur'),
    url(r'^shopping_num/',views.shopping_num,name='shopping_num' ),
]