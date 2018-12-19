from django.db import models
from manageuser.models import Manage_goods,Manage_shop
from manageuser.models import Manage
from users.models import User
# Create your models here.
class cart(models.Model):
    cart_id=models.AutoField(auto_created=True,primary_key=True,db_column='cart_id')
    manage=models.ForeignKey(Manage,null=False,db_column='manage_id')
    goods=models.ForeignKey(Manage_goods,null=False,db_column='goods_id')
    user=models.ForeignKey(User,null=False,db_column='user_id')
    goods_name=models.CharField(max_length=100,null=False,db_column='goods_name')
    goods_pic = models.CharField(max_length=100, null=False, db_column='goods_pic')
    goods_price = models.FloatField(null=False, db_column='goods_price')
    goods_sum = models.FloatField(null=False, db_column='goods_sum')
    goods_num = models.IntegerField(null=False, db_column='goods_num')
    shop=models.ForeignKey(Manage_shop,null=False,db_column='shop_id')