from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from utils.pay import AliPay
from urllib.parse import parse_qs
from order.models import Order_page,Oreder
import random
# Create your views here.
def play(request):
    sum=request.POST['order_sum']
    num = request.POST['order_num']
    name = request.POST['address_name']
    return HttpResponse('下单成功')

def play_han(request):
    pass

def get_ali_object(num):
    #沙箱appID
    app_id="2016092400585217"
    #支付完成后，想这里发送请求
    notify_url="http://127.0.0.1:8000/playhan"
    #支付完成后跳转的地址
    return_url="http://127.0.0.1:8000/play_success?num="+str(num)
    merchant_private_Key_path="keys/app_private_2048.txt"
    alipay_public_Key_path = "keys/alipay_public_2048.txt"
    alipay=AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_Key_path,
        alipay_public_key_path=alipay_public_Key_path,
        debug=True,
    )
    return alipay
def get_ali_object_one(num):
    #沙箱appID
    app_id="2016092400585217"
    #支付完成后，想这里发送请求
    notify_url="http://127.0.0.1:8000/playhan"
    #支付完成后跳转的地址
    return_url="http://127.0.0.1:8000/play_success_one?num="+str(num)
    merchant_private_Key_path="keys/app_private_2048.txt"
    alipay_public_Key_path = "keys/alipay_public_2048.txt"
    alipay=AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_Key_path,
        alipay_public_key_path=alipay_public_Key_path,
        debug=True,
    )
    return alipay

def playhan(request):
    alipay=get_ali_object()
    if request.method=="POST":
        #检测是否支付成功
        #去请求中获取所有返回的数据：状态/订单号
        body_str=request.body.decode("utf-8")
        post_data=parse_qs(body_str)
        post_dict={}
        for k,v in post_data.items():
            post_dict[k]=v[0]
        sign=post_dict.pop('sign',None)
        status=alipay.verify(post_dict,sign)
        print("___123_____")
        print("___123_____")
        print("___123_____")
        out_trade_no=post_dict['out_trade_no']
        print("结束")
        return HttpResponse('POST返回')
    else:
        params=request.GET.dict()
        sign=params.pop('sign',None)
        status=alipay.verify(params,sign)
        print("___123_____")
        print("___123_____")
        print("___123_____")
        return HttpResponse('支付成功')
def payorder(request):
    money=float(request.POST.get('order_sum'))
    id=request.POST['order_id']
    alipay=get_ali_object_one(id)
    query_params=alipay.direct_pay(
        subject="我的大叔",
        out_trade_no=request.POST['order_num'],
        total_amount=money,
    )
    pay_url="https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)
    return HttpResponseRedirect(pay_url)

def pay_continue(request,pk):
    #个人支付
    result=Oreder.objects.get(pk=pk)
    money=result.order_sum
    num=result.order_num
    alipay = get_ali_object_one(pk)
    query_params = alipay.direct_pay(
        subject="我的大叔",
        out_trade_no=num,
        total_amount=money,
    )
    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)
    return HttpResponseRedirect(pay_url)
def play_shopping(request):
    # 购物车支付
    # money = float(request.POST.get('order_sum'))
    id = request.POST.getlist('id','')
    print(id)
    sum=0
    for i in id:
        sum+=Oreder.objects.get(pk=i).order_sum
    print(sum)
    alipay = get_ali_object(id)
    query_params = alipay.direct_pay(
        subject="我的大叔",
        out_trade_no=random.randrange(1,10000000000),
        total_amount=sum,
    )
    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)
    # result = Oreder.objects.get(order_id=id)
    # result.order_state = 0
    # result.save()
    return HttpResponseRedirect(pay_url)
def play_success(request):
    num=request.GET.get('num',1)
    num=eval(num)
    for number in num:
        i=Oreder.objects.get(pk=number)
        i.order_state=0
        i.save()
    return HttpResponseRedirect('/user_order')

def play_success_one(request):
    num=request.GET.get('num',1)
    print(num)
    result=Oreder.objects.get(pk=int(num))
    result.order_state=0
    result.save()
    return HttpResponseRedirect('/user_order')