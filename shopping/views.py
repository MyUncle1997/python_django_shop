from django.shortcuts import render
import functools
import json
from .models import cart
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum
from manageuser.models import Manage_goods
from manageuser.models import Manage_goods, Manage_shop


# Create your views here.
def show(num):
    @functools.wraps(num)
    def run(request, *arg, **kw):
        if 'user' in request.session:
            return num(request, *arg, **kw)
        else:
            return HttpResponseRedirect('/login')

    return run


@show
def shopping_user(request):
    # 用户购物车
    num = set()
    shop = []
    result_shop = cart.objects.values('shop_id')
    for i in result_shop:
        num.add(i['shop_id'])
    for i in num:
        shop.append(Manage_shop.objects.get(pk=i))
    result = cart.objects.filter(user_id=request.session['user_id']).all()
    # sum = cart.objects.filter(user_id=request.session['user_id']).aggregate(total=Sum('goods_sum'))
    return render(request, 'Reception/shopping/shopping_user.html',{'sp_list': result, 'sum': 0, 'shop': shop})
def shopping_add(request):
    # 添加购物车
    try:
        user_id = request.session['user_id']
        manager_id = request.POST['manager_id']
        goods_id = request.POST['goods_id']
        goods_name = request.POST['goods_name']
        goods_pic = request.POST['goods_pic']
        goods_price = request.POST['goods_price']
        goods_num = request.POST['goods_num']
        shop_id = request.POST['shop_id']
        goods_sum = float(goods_price) * float(goods_num)
        goods_count = cart.objects.filter(goods_id=goods_id).count()
        if goods_count > 0:
            result_get = cart.objects.get(goods_id=goods_id)
            result_get.goods_num = int(result_get.goods_num) + int(goods_num)
            result_get.goods_sum = float(goods_price) * float(result_get.goods_num)
            result_get.save()
        else:
            result = cart.objects.create(
                goods_name=goods_name,
                goods_pic=goods_pic,
                goods_price=goods_price,
                goods_num=goods_num,
                goods_sum=goods_sum,
                user_id=user_id,
                manage_id=manager_id,
                goods_id=goods_id,
                shop_id=shop_id
            )
        return HttpResponse(1)
    except:
        return HttpResponse(0)


def shopping_del(request, pk):
    # 商品删除
    result = cart.objects.get(pk=pk)
    result.delete()
    return HttpResponse(pk)


def shopping_w_del(request):
    # 商品全部删除
    result = cart.objects.filter(user_id=request.session['user_id']).all()
    result.delete()
    return HttpResponseRedirect('/shopping_user')


def shopping_plus(request, pk):
    # 购物车增加操作
    result = cart.objects.get(user_id=request.session['user_id'], goods_id=pk)
    goods_get = Manage_goods.objects.get(pk=pk)
    result.goods_num += 1
    if result.goods_num > goods_get.goods_count:
        result.goods_num = goods_get.goods_count
    else:
        result.goods_sum = result.goods_sum + result.goods_price
    result.save()
    num = int(request.GET.get('num', 1)) + 1
    if num > goods_get.goods_count:
        num = goods_get.goods_count
    sum_int = cart.objects.aggregate(total=Sum('goods_sum'))['total']
    sum_one = cart.objects.get(goods_id=pk).goods_sum
    return_json = {'result': num, 'sum': sum_int, 'sum_one': sum_one}
    return HttpResponse(json.dumps(return_json), content_type='application/json')
    # result=cart.objects.get(user_id=request.session['user_id'],goods_id=pk)
    # goods_get=Manage_goods.objects.get(pk=pk)
    #
    # result.goods_num+=1
    # if result.goods_num>goods_get.goods_count:
    #     result.goods_num=goods_get.goods_count
    # else:
    #     result.goods_sum = result.goods_sum + result.goods_price
    # result.save()
    # return HttpResponseRedirect('/shopping_user')


def shopping_re(request, pk):
    # 购物车减少操作
    result = cart.objects.get(user_id=request.session['user_id'], goods_id=pk)
    result.goods_num -= 1
    if result.goods_num < 1:
        result.goods_num = 1
        result.goods_sum = result.goods_price
    else:
        result.goods_sum = result.goods_sum - result.goods_price
    result.save()
    num = int(request.GET.get('num', 1)) - 1
    if num < 1:
        num = 1
    sum_int = cart.objects.aggregate(total=Sum('goods_sum'))['total']
    sum_one = cart.objects.get(goods_id=pk).goods_sum
    return_json = {'result': num, 'sum': sum_int, 'sum_one': sum_one}
    return HttpResponse(json.dumps(return_json), content_type='application/json')


def shopping_blur(request, pk):
    # 失去焦点
    result = cart.objects.get(user_id=request.session['user_id'], goods_id=pk)
    goods_get = Manage_goods.objects.get(pk=pk)
    # result.goods_num -= 1
    # if result.goods_num < 1:
    #     result.goods_num = 1
    #     #     result.goods_sum = result.goods_price
    #     # else:
    #     #     result.goods_sum = result.goods_sum - result.goods_price
    #     # result.save()
    num = int(request.GET.get('num', 1))
    # print(num)
    if num < 1:
        num = 1
    elif num > goods_get.goods_count:
        num = goods_get.goods_count
    result.goods_sum = result.goods_price * num
    result.goods_num = num
    result.save()
    sum_int = cart.objects.aggregate(total=Sum('goods_sum'))['total']
    sum_one = cart.objects.get(goods_id=pk).goods_sum
    return_json = {'result': num, 'sum': sum_int, 'sum_one': sum_one}
    return HttpResponse(json.dumps(return_json), content_type='application/json')
def shopping_num(request):
    num=int(request.GET.get('num',0))
    if num==1:
        sum = cart.objects.filter(user_id=request.session['user_id']).aggregate(total=Sum('goods_sum'))['total']
        return HttpResponse(sum)
    else:
        return HttpResponse(0)
