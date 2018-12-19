from django.shortcuts import render
import functools
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import Oreder,Order_page,Address
from shopping.models import cart
from django.db.models import Sum
from manageuser.models import Manage_goods
import random
from datetime import datetime
import time
# Create your views here.
def show(num):
    @functools.wraps(num)
    def run(request,*arg,**kw):
        if 'user' in request.session:
            return num(request,*arg,**kw)
        else:
            return HttpResponseRedirect('/login')
    return run
@show
def order(request):
    #购物车下单
    id=request.POST.getlist('sp_che')
    result=cart.objects.filter(cart_id__in=id)
    result_ad=Address.objects.filter(user_id=request.session['user_id'])
    sum = cart.objects.filter(cart_id__in=id).aggregate(total=Sum('goods_sum'))
    return render(request, 'Reception/order/order_shopping.html', {'list':result, 'list_ad':result_ad, 'sum':sum['total']})
def order_check(request):
    #勾选下单
    num=request.GET.get('num')
    state=request.GET.get('state')
    if state=='true':
        sum = cart.objects.filter(pk=num).aggregate(total=Sum('goods_sum'))['total']
        state = 1
        print(sum)
        return JsonResponse({'sum':sum,'state':state})
    else:
        sum = cart.objects.filter(pk=num).aggregate(total=Sum('goods_sum'))['total']
        state = 0
        return JsonResponse({'sum': sum, 'state': state})
@show
def order_dowm(request):
    #用户下单
    id=request.POST['goods_id']
    num=request.POST['num']
    shop_id = request.POST['shop_id']
    result=Manage_goods.objects.get(pk=id)
    result_ad = Address.objects.filter(user_id=request.session['user_id'])
    sum=int(num)*float(result.goods_xprice)
    return render(request, 'Reception/order/order_down.html', {'goods':result, 'num':num,'address':result_ad,'sum':sum})
def order_han(request):
    #购物车订单处理
    result=Address.objects.filter(user_id=request.session['user_id']).count()
    if result>0:
        address_id = request.POST['address_id']
        user_id = request.session['user_id']
        cart_id=request.POST.getlist('sp_id')
        request.session['cart_id']=cart_id
        num = set()
        result_shop = cart.objects.filter(cart_id__in=cart_id).values('shop_id')
        for i in result_shop:
            num.add(i['shop_id'])
        for i in num:
            sum=cart.objects.filter(shop_id=i,cart_id__in=cart_id).aggregate(total=Sum('goods_sum'))['total']
        # shop_id=request.POST['shop_id']
        # request.session['user_shop_id']=shop_id
            order_time=datetime.now()
            order_num=str(int(time.time()))+str(random.randrange(1000000))+str(i)
            result=Oreder.objects.create(
                order_num=int(order_num),
                order_sum=float(sum),
                address_id=address_id,
                user_id=user_id,
                order_time=order_time,
                order_state=10,
                shop_id=i
            )
        return HttpResponseRedirect('/order_save')
    else:
        return HttpResponse('请先添加地址')
def order_save(request):
    #购物车订单保存
    num = set()
    result_shop = cart.objects.filter(cart_id__in=request.session['cart_id']).values('shop_id')
    for i in result_shop:
        num.add(i['shop_id'])
    request.session['order_num']=len(num)
    der=Oreder.objects.filter(user_id=request.session['user_id']).order_by('-order_id')[:len(num)]
    for num in der:
        cart_get=cart.objects.raw("select * from shopping_cart join manageuser_manage_goods on shopping_cart.goods_id=manageuser_manage_goods.goods_id where shopping_cart.shop_id="+str(num.shop_id))
        for i in cart_get:
            result=Order_page.objects.create(
                goods_id=i.goods_id,
                goods_name=i.goods_name,
                goods_pic=i.goods_pic,
                goods_sum=i.goods_sum,
                goods_num=i.goods_num,
                manage_id=i.manage_id,
                order_id=num.order_id,
                manage_price=i.goods_xprice,
                shop_id=i.shop_id,
                order_number=str(int(time.time()))+str(random.randrange(1000000))+str(i.manage_id)

            )
    if num:
        return HttpResponseRedirect('/order_success')
def order_success(request):
    #数量减少
    if request.session['order_num']>1:
        der = Oreder.objects.filter(user_id=request.session['user_id']).order_by('-order_id')[:request.session['order_num']]
        order_num=[]
        order_num_new=[]
        for i in der:
            order_num.append(i.order_id)
        for i in order_num:
            order_num_new.append(Order_page.objects.filter(order_id=i))
        for i in order_num_new:
            for num in i:
                sum=Manage_goods.objects.get(goods_id=num.goods_id)
                sum.goods_count=sum.goods_count - num.goods_num
                sum.save()
    else:
        der = Oreder.objects.filter(user_id=request.session['user_id']).last()
        result=Order_page.objects.filter(order_id=der.order_id)
        for num in result:
            sum = Manage_goods.objects.get(goods_id=num.goods_id)
            sum.goods_count = sum.goods_count - num.goods_num
            sum.save()
    #下单成功
    result=Oreder.objects.filter(user_id=request.session['user_id']).order_by('-order_id')[:request.session['order_num']]
    # address_id=result.address_id
    add=Address.objects.all()
    if result:
        cart_get=cart.objects.filter(cart_id__in=request.session['cart_id'])
        cart_get.delete()
        return render(request,'Reception/order/order_success.html',{'list1':result,'address':add})
@show
def order_address(request):
    #地址添加页面
    return render(request,'Reception/order/order_address.html')
@show
def order_address_han(request):
    #地址添加
    if 'user' in request.session:
        name=request.POST['username']
        phone=request.POST['phone']
        address=request.POST['address']
        result=Address.objects.create(
            address_username=name,
            address_phone=phone,
            address_name=address,
            user_id=request.session['user_id']
        )
    return HttpResponseRedirect('/order')

def order_dowm_user(request):
    #用户下单
    result = Address.objects.filter(user_id=request.session['user_id']).count()
    if result > 0:
        address_id = request.POST['address_id']
        sum = request.POST['sum']
        request.session['order_id']=request.POST['goods_id']
        request.session['shop_dowm'] = request.POST['shop_id']
        request.session['order_num'] = request.POST['num']
        user_id = request.session['user_id']
        order_time = datetime.now()
        order_num = int(time.time())
        result = Oreder.objects.create(
            order_num=str(int(time.time())) + str(random.randrange(1000000)) + str(user_id),
            order_sum=float(sum),
            address_id=address_id,
            user_id=user_id,
            order_time=order_time,
            order_state=10,
            shop_id=request.session['shop_dowm']
        )
        if result:
            return HttpResponseRedirect('/order_dowm_user_han')
    else:
        return HttpResponse('请先添加地址')
def order_dowm_user_han(request):
    #用户订单保存
    der = Oreder.objects.filter(user_id=request.session['user_id']).last()
    order = der.order_id
    sum=der.order_sum
    goods=Manage_goods.objects.get(pk=request.session['order_id'])
    result = Order_page.objects.create(
        goods_id=request.session['order_id'],
        goods_name=goods.goods_name,
        goods_pic=goods.goods_pic,
        goods_sum=sum,
        goods_num=request.session['order_num'],
        manage_id=goods.manager_id,
        order_id=order,
        manage_price=goods.goods_xprice,
        shop_id=request.session['shop_dowm'],
        order_number = str(int(time.time())) + str(random.randrange(1000000)) + str(order)
    )
    if result:
        return HttpResponseRedirect('/order_user_success')
def order_user_success(request):
    #用户下单成功
    result = Oreder.objects.filter(user_id=request.session['user_id']).last()
    order_id=result.order_id
    result_page=Order_page.objects.get(order_id=order_id)
    result_goods=Manage_goods.objects.get(pk=result_page.goods_id)
    result_goods.goods_count=result_goods.goods_count - result_page.goods_num
    result_goods.save()
    address_id = result.address_id
    add = Address.objects.get(pk=address_id)
    return render(request,'Reception/order/user_dowm_success.html',{'list':result,'address':add})

