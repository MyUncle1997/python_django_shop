from django.db import models
from users.models import User,User_comment
from manageuser.models import Manage_goods,Manage,Manage_shop
# Create your models here.
#地址表
class Address(models.Model):
    address_id=models.AutoField(auto_created=True,primary_key=True,db_column='address_id')
    user=models.ForeignKey(User,null=False,db_column='user_id')
    address_username=models.CharField(max_length=20,null=False,db_column='address_username')
    address_phone=models.IntegerField(null=False,db_column='address_phone')
    address_name=models.CharField(max_length=100,null=False,db_column='address_name')

#订单表
class Oreder(models.Model):
    order_id=models.AutoField(auto_created=True,primary_key=True,db_column='order_id')
    user=models.ForeignKey(User,null=False,db_column='user_id')
    order_num=models.CharField(max_length=30,null=False,db_column='order_num')
    order_time=models.DateTimeField(null=False,db_column='order_time')
    send_time = models.DateTimeField(null=False, db_column='send_time')
    recv_time = models.DateTimeField(null=False, db_column='recv_time')
    address=models.ForeignKey(Address,null=False,db_column='address_id')
    order_sum=models.FloatField(null=False,db_column='order_sum')
    order_state = models.IntegerField(null=False, db_column='order_state')
    shop=models.ForeignKey(Manage_shop,null=False,db_column='shop_id')
#订单详情页
class Order_page(models.Model):
    order_page_id=models.AutoField(auto_created=True,primary_key=True,db_column='order_page_id')
    goods=models.ForeignKey(Manage_goods,null=False,db_column='goods_id')
    goods_name=models.CharField(max_length=30,null=False,db_column='goods_name')
    goods_pic=models.CharField(max_length=100,null=False,db_column='goods_pic')
    manage_price=models.FloatField(null=False,db_column='manage_price')
    goods_sum=models.FloatField(null=False,db_column='goods_sum')
    goods_num=models.IntegerField(null=False,db_column='goods_num')
    manage=models.ForeignKey(Manage,db_column='manage_id')
    order=models.ForeignKey(Oreder,null=False,db_column='order_id')
    shop = models.ForeignKey(Manage_shop, null=False, db_column='shop_id')
    order_number = models.CharField(max_length=30, null=False, db_column='order_number')