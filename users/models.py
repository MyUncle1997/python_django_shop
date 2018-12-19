from django.db import models
from manageuser.models import Manage_goods,Manage
# Create your models here.
#用户表
class User(models.Model):
    user_id=models.AutoField(auto_created=True,primary_key=True,db_column='user_id')
    username=models.CharField(max_length=20,null=False,db_column='username')
    password = models.CharField(max_length=32, null=False,db_column='password')
    email=models.CharField(max_length=50,null=True,db_column='email')
    sex=models.CharField(max_length=5,null=True,db_column='sex')
    age=models.IntegerField(null=True,db_column='age')
    body=models.TextField(null=True,db_column='body')
    pic=models.ImageField(null=True,db_column='pic')
    state=models.IntegerField(null=False,db_column='state')
#用户评论表
class User_comment(models.Model):
    user_comment_id=models.AutoField(auto_created=True,primary_key=True,db_column='user_comment_id')
    goods =models.ForeignKey(Manage_goods,null=False,db_column='goods_id')
    user = models.ForeignKey(User, null=False, db_column='user_id')
    manage = models.ForeignKey(Manage, null=False, db_column='manage_id')
    comment_time=models.DateTimeField(null=False,db_column='comment_time')
    comment_body = models.TextField(null=False, db_column='comment_body')
    order_id=models.IntegerField(null=False,db_column='order_id')
    order_page_id = models.IntegerField(null=False, db_column='order_page_id')

#用户邮箱记录
class User_email(models.Model):
    email_id=models.AutoField(auto_created=True,primary_key=True,db_column='email_id')
    email_time=models.DateTimeField(null=False,db_column='email_time')
    email_body=models.TextField(null=False,db_column='email_body')
    email_title=models.CharField(max_length=50,null=False,db_column='email_title')
    user=models.ForeignKey(User,null=False,db_column='user_id')

#收藏记录
class User_collection(models.Model):
    collection_id=models.AutoField(auto_created=True,primary_key=True,db_column='collection_id')
    goods=models.ForeignKey(Manage_goods,null=False,db_column="goods_id")
    user=models.ForeignKey(User,null=False,db_column="user_id")