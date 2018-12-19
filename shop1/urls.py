"""shop1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from .upload import upload_image
from django.conf import settings

urlpatterns = [
    #首页
    url(r'', include('goods.urls',namespace='goods')),
    #用户中心
    url(r'',include('users.urls',namespace='users')),
    #购物车中心
    url(r'',include('shopping.urls',namespace='shopping')),
    #商品详情页中心
    url(r'',include('dtpage.urls',namespace='dtpage')),
    #商品分类
    url(r'',include('type.urls',namespace='type')),
    #订单中心
    url(r'',include('order.urls',namespace='order')),
    #商家后台
    url(r'',include('manageuser.urls',namespace='manage')),
    #支付功能
    url(r'',include('play.urls',namespace='play')),
    #商家中心
    url(r'',include('shop.urls',namespace='shop')),
    #kindeditor编辑图片处理
    url(r'^admin/uploads/(?P<dir_name>[^/]+)$',upload_image,name='upload_image'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
