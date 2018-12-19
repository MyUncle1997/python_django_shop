from django.db import models
# Create your models here.
#商家表
class Manage(models.Model):
    manage_id=models.AutoField(auto_created=True,primary_key=True,db_column='manage_id')
    manage_name=models.CharField(max_length=30,null=True,db_column='manage_name')
    manage_pass = models.CharField(max_length=30,null=True,db_column='manage_pass')
    manage_role=models.ForeignKey('Manage_role',default=1)

#店铺表
class Manage_shop(models.Model):
    manage_shop_id = models.AutoField(auto_created=True, primary_key=True, db_column='manage_shop_id')
    manage_shop_name =models.CharField(max_length=30,null=False,db_column='manage_shop_name')
    manage_shop_address = models.CharField(max_length=50,null=False,db_column='manage_shop_address')
    manage = models.ForeignKey(Manage,null=False,db_column='manage_id')
    manage_shop_time = models.DateTimeField(null=False,db_column='manage_shop_time')
    manage_shop_pic = models.ImageField(max_length=100,null=False,db_column='manage_shop_pic')
    manage_shop_username=models.CharField(max_length=30,null=False,db_column='manage_shop_username')
#商品分类表
class Manage_type(models.Model):
    type_id=models.AutoField(auto_created=True,primary_key=True,db_column="type_id")
    type_name = models.CharField(max_length=30, db_column='type_name')
    shop=models.ForeignKey(Manage_shop,null=False,db_column='shop_id')


#商品表
class Manage_goods(models.Model):
    goods_id=models.AutoField(auto_created=True,primary_key=True,db_column='goods_id')
    goods_num=models.CharField(max_length=30,null=False,db_column='goods_num')
    goods_name = models.CharField(max_length=30,null=False,db_column='goods_name')
    type=models.ForeignKey(Manage_type,db_column='type_id')
    goods_oprice=models.IntegerField(null=False,db_column='goods_oprice')
    goods_xprice = models.IntegerField(null=False, db_column='goods_xprice')
    goods_count = models.IntegerField(null=False, db_column='goods_count')
    goods_method=models.CharField(max_length=200,null=False,db_column='goods_method')
    goods_infro = models.CharField(max_length=200, null=False, db_column='goods_infro')
    goods_ishow = models.IntegerField(null=False, db_column='goods_ishow')
    goods_pic=models.ImageField(default="",upload_to="media/uploads")
    goods_address=models.CharField(max_length=200, null=False, db_column='goods_address')
    goods_body=models.CharField(max_length=3000, null=False, db_column='goods_body')
    manager=models.ForeignKey(Manage,db_column='manager_id')
    up_time=models.DateTimeField(null=False, db_column='goods_up_time')
    dowm_time = models.DateTimeField(null=True, db_column='goods_down_time')
    shop=models.ForeignKey(Manage_shop,null=False,db_column='shop_id')

#物流功能
class Logistics(models.Model):
    logistics_id=models.AutoField(auto_created=True,primary_key=True,db_column='logistics_id')
    logistics_name=models.CharField(max_length=20,null=False,db_column='logistics_name')
    logistics_time=models.DateTimeField(null=False,db_column='logistics_time')
    logistics_num = models.CharField(max_length=50,null=False,db_column='logistics_num')
    user=models.IntegerField(null=False,db_column='user_id')
    order= models.IntegerField(null=False, db_column='order_id')

#权限列表
class Manage_power(models.Model):
    power_name=models.CharField(max_length=30,null=False,db_column='power_name')
    power_url=models.CharField(max_length=50,null=False,db_column='power_url')
    power_namespace=models.CharField(max_length=30,null=False,db_column='power_namespace')

#角色列表
class Manage_role(models.Model):
    role_name=models.CharField(max_length=20,null=False,db_column='role_name')
    add_time=models.DateTimeField(auto_now_add=True)
    power=models.ManyToManyField('Manage_power')
    add_user=models.CharField(max_length=30,null=False,db_column='add_user')
    status = models.SmallIntegerField(null=False,db_column='status')