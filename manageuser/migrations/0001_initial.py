# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-13 16:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logistics',
            fields=[
                ('logistics_id', models.AutoField(auto_created=True, db_column='logistics_id', primary_key=True, serialize=False)),
                ('logistics_name', models.CharField(db_column='logistics_name', max_length=20)),
                ('logistics_time', models.DateTimeField(db_column='logistics_time')),
                ('logistics_num', models.CharField(db_column='logistics_num', max_length=50)),
                ('user', models.IntegerField(db_column='user_id')),
                ('order', models.IntegerField(db_column='order_id')),
            ],
        ),
        migrations.CreateModel(
            name='Manage',
            fields=[
                ('manage_id', models.AutoField(auto_created=True, db_column='manage_id', primary_key=True, serialize=False)),
                ('manage_name', models.CharField(db_column='manage_name', max_length=30, null=True)),
                ('manage_pass', models.CharField(db_column='manage_pass', max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manage_goods',
            fields=[
                ('goods_id', models.AutoField(auto_created=True, db_column='goods_id', primary_key=True, serialize=False)),
                ('goods_num', models.CharField(db_column='goods_num', max_length=30)),
                ('goods_name', models.CharField(db_column='goods_name', max_length=30)),
                ('goods_oprice', models.IntegerField(db_column='goods_oprice')),
                ('goods_xprice', models.IntegerField(db_column='goods_xprice')),
                ('goods_count', models.IntegerField(db_column='goods_count')),
                ('goods_method', models.CharField(db_column='goods_method', max_length=200)),
                ('goods_infro', models.CharField(db_column='goods_infro', max_length=200)),
                ('goods_ishow', models.IntegerField(db_column='goods_ishow')),
                ('goods_pic', models.ImageField(default='', upload_to='media/uploads')),
                ('goods_address', models.CharField(db_column='goods_address', max_length=200)),
                ('goods_body', models.CharField(db_column='goods_body', max_length=200)),
                ('up_time', models.DateTimeField(db_column='goods_up_time')),
                ('dowm_time', models.DateTimeField(db_column='goods_down_time', null=True)),
                ('manager', models.ForeignKey(db_column='manager_id', on_delete=django.db.models.deletion.CASCADE, to='manageuser.Manage')),
            ],
        ),
        migrations.CreateModel(
            name='Manage_shop',
            fields=[
                ('manage_shop_id', models.AutoField(auto_created=True, db_column='manage_shop_id', primary_key=True, serialize=False)),
                ('manage_shop_name', models.CharField(db_column='manage_shop_name', max_length=30)),
                ('manage_shop_address', models.CharField(db_column='manage_shop_address', max_length=50)),
                ('manage_shop_time', models.DateTimeField(db_column='manage_shop_time')),
                ('manage_shop_pic', models.ImageField(db_column='manage_shop_pic', upload_to='')),
                ('manage_shop_username', models.CharField(db_column='manage_shop_username', max_length=30)),
                ('manage', models.ForeignKey(db_column='manage_id', on_delete=django.db.models.deletion.CASCADE, to='manageuser.Manage')),
            ],
        ),
        migrations.CreateModel(
            name='Manage_type',
            fields=[
                ('type_id', models.AutoField(auto_created=True, db_column='type_id', primary_key=True, serialize=False)),
                ('type_name', models.CharField(db_column='type_name', max_length=30)),
                ('shop', models.ForeignKey(db_column='shop_id', on_delete=django.db.models.deletion.CASCADE, to='manageuser.Manage_shop')),
            ],
        ),
        migrations.AddField(
            model_name='manage_goods',
            name='shop',
            field=models.ForeignKey(db_column='shop_id', on_delete=django.db.models.deletion.CASCADE, to='manageuser.Manage_shop'),
        ),
        migrations.AddField(
            model_name='manage_goods',
            name='type',
            field=models.ForeignKey(db_column='type_id', on_delete=django.db.models.deletion.CASCADE, to='manageuser.Manage_type'),
        ),
    ]
