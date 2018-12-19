from django.shortcuts import render
from manageuser.models import Manage_goods,Manage_shop,Manage_type
from users.models import User_comment,User,User_collection
from order.models import Oreder,Order_page
import functools
from django.http import HttpResponse,HttpResponseRedirect
import json
# Create your views here.
def show(num):
    @functools.wraps(num)
    def run(request,*arg,**kw):
        if 'user' in request.session:
            return num(request,*arg,**kw)
        else:
            return HttpResponseRedirect('/login')
    return run
def dtpage(request,pk):
    num=[]
    result = Manage_goods.objects.get(pk=pk)
    #店铺的其他商品
    count= Manage_goods.objects.filter(shop_id=result.shop_id).exclude(goods_id=pk)[0:4]
    comment=User_comment.objects.filter(goods_id=pk)
    for i in comment:
        num.append(User.objects.get(user_id=i.user_id))
    sql='SELECT * FROM users_user_comment f join users_user g on f.user_id=g.user_id where f.goods_id='+str(pk)
    combine=User_comment.objects.raw(sql)
    #店铺分类
    result_type=Manage_type.objects.filter(shop_id=result.shop_id)
    #统计多少人购买
    sql='SELECT COUNT(goods_id) num,goods_id,g.order_id FROM order_oreder g INNER JOIN order_order_page f on g.order_id=f.order_id GROUP BY f.goods_id HAVING f.goods_id='+str(pk)
    result_num=Oreder.objects.raw(sql)
    #统计评论数
    count_comment=User_comment.objects.filter(goods_id=pk).count()
    return render(request,'Reception/dtpage/index.html',{'list':result,'count':count,'comment':comment,'num':combine,'re_ty':result_type,'pur_num':result_num,'count_comment':count_comment})
def dtpage_collection(request,pk):
    print(pk)
    try:
        result=User_collection.objects.filter(user_id=request.session['user_id'],goods_id=pk)
        if result:
            result_json = {'text': '你已经收藏了'}
            return HttpResponse(json.dumps(result_json), content_type='application/json')
        else:
            result_json = {'text': '收藏成功'}
            User_collection.objects.create(user_id=request.session['user_id'],goods_id=pk)
            return HttpResponse(json.dumps(result_json), content_type='application/json')
    except:
        result_json={'text':'请登录再收藏'}
        return HttpResponse(json.dumps(result_json),content_type='application/json')