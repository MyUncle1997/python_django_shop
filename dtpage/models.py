from django.db import models
# from manageuser.models import Manage_goods,Manage
# from users.models import User
# Create your models here.
# 用户评论表
# class Comment(models.Model):
#     comment_id = models.AutoField(auto_created=True, null=True, db_column='comment_id')
#     goods=models.ForeignKey(Manage_goods,null=False,db_column='goods_id')
#     user=models.ForeignKey(User,null=False,db_column='user_id')
#     manage=models.ForeignKey(Manage,null=False,db_column='manage_id')
#     comment_time=models.DateTimeField(null=False,db_column='comment_time')
#     comment_body=models.TextField(null=False,db_column='comment_body')
