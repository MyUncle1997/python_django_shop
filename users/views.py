from django.shortcuts import render
from .models import User,User_comment,User_email,User_collection
import functools
from manageuser.models import Logistics
from manageuser.models import Manage_goods,Manage
from django.db.models import Sum
from order.models import Oreder,Order_page,Address
from django.http import HttpResponse,HttpResponseRedirect
from datetime import  datetime
from shop1 import settings
from django.core.mail import send_mail
import json
import hashlib
import time
import sched
# Create your views here.
def show(num):
    @functools.wraps(num)
    def run(request,*arg,**kw):
        if 'user' in request.session:
            return num(request,*arg,**kw)
        else:
            return HttpResponseRedirect('/login')
    return run
def register(request):
    #用户注册页面
    return render(request, 'Reception/users/register.html')
def register_handel(request):
    #用户注册验证
    name=request.POST['user']
    password=request.POST['passwd']
    email=request.POST['email']
    try:
        result=User.objects.get(username=name)
        if result:
            return HttpResponse('已存在用户，请重新注册')
    except:
        code=request.POST['code']
        Code=request.session['Code']
        if code.lower()==Code.lower():
            hash = hashlib.md5()
            hash.update(bytes(password, encoding='utf-8'))
            result = User.objects.create(username=name, password=hash.hexdigest(),state=0,email=email)
            return HttpResponseRedirect('/user_activation')
        elif code.lower()!=Code.lower():
            return HttpResponse('验证码错误')
        else:
            return HttpResponse('失败')
def login(request):
    #用户登录验证
    next=request.GET.get('next','next')
    print(next)
    return render(request, 'Reception/users/login.html',{'next':next})
def login_handel(request):
    #用户登录处理
    name=request.POST['user']
    password=request.POST['passwd']
    next=request.POST['next']
    code=request.POST['code']
    Code=request.session['Code']
    hash = hashlib.md5()
    hash.update(bytes(password, encoding='utf-8'))
    result=User.objects.filter(username=name,password=hash.hexdigest())
    if result:
        id = User.objects.get(username=name, password=hash.hexdigest()).state
        if id==1:
            if code.lower()==Code.lower():
                id=User.objects.get(username=name,password=hash.hexdigest()).user_id
                img=User.objects.get(username=name,password=hash.hexdigest()).pic
                new_img=str(img)
                request.session['user']=name
                request.session['user_pic']=new_img
                request.session['user_id']=id
                request.session.set_expiry(500)
                if next=='next':
                    data = {'num': 3, 'text': '/goods'}
                    return HttpResponse(json.dumps(data))
                else:
                    data = {'num': 4, 'text': next}
                    return HttpResponse(json.dumps(data))
            else:
                data={'num':0,'text':'验证码错误'}
                return HttpResponse(json.dumps(data))
        else:
            data = {'num': 2, 'text': '账号未激活'}
            return HttpResponse(json.dumps(data))
    else:
        data = {'num': 1, 'text': '用户名或密码错误'}
        return HttpResponse(json.dumps(data))
def login_quit(request):
    #用户注销登录
    del request.session['user']
    del request.session['user_id']
    return HttpResponseRedirect('/goods')
#用户后台
@show
def user_order(request):
    #用户订单中心
    try:
        result=Oreder.objects.filter(user_id=request.session['user_id']).last()
        # ord=int(result.oreder_id)
        result1 = Oreder.objects.filter(user_id=request.session['user_id']).order_by('-order_id')
        num=Order_page.objects.all()
        # for i in result1:
        #     ord = int(i.order_id)
        #     page=Order_page.objects.filter(order_id=ord)
        #     num.append(page)
        # list=zip(num,result1)
        return render(request,'Reception/users/user_order.html',{'list':result1,'num':num})
    except:
        return render(request,'Reception/goods/index.html')
@show
def user_order_confirm(request,pk):
    #确认收货操作
    result=Oreder.objects.filter(pk=pk).update(order_state=2,recv_time=datetime.now())
    return HttpResponseRedirect('/user_order')
@show
def user_order_pg(request,pk):
    #订单详情页
    result=Oreder.objects.get(order_id=pk)
    address=Address.objects.get(pk=result.address_id)
    result_page=Order_page.objects.filter(order_id=pk)
    sum=Order_page.objects.filter(order_id=pk).aggregate(total=Sum('goods_sum'))
    return render(request,'Reception/users/user_order_pg.html',{'list':result,'num':result_page,'sum':sum['total'],'address':address})
@show
def user_modify(request):
    #修改密码页面
    return render(request,'Reception/users/user_modify.html')
@show
def user_modify_han(request):
    #修改密码

    o_pass=request.POST['opass']
    new_pass = request.POST['new_pass']
    new_pass2 = request.POST['new_pass2']
    hash = hashlib.md5()
    hash.update(bytes(o_pass, encoding='utf-8'))
    new_hash=hashlib.md5()
    new_hash.update(bytes(new_pass, encoding='utf-8'))
    result=User.objects.get(pk=request.session['user_id'])
    x_result=result.password
    if hash.hexdigest()==x_result:
        if new_pass==new_pass2:
            new_result=User.objects.filter(username=request.session['user']).update(password=new_hash.hexdigest())
            del request.session['user']
            del request.session['user_id']
            return HttpResponseRedirect('/login')
        else:
            return  HttpResponse('两次输入的密码不一致，请返回重新修改')
    else:
        return HttpResponse('旧密码输入不对，请重新输入')
@show
def user_address(request):
    #地址页面
    result=Address.objects.filter(user_id=request.session['user_id'])
    return render(request,'Reception/users/user_address.html',{'list':result})
@show
def user_address_modify(request,pk):
    #地址修改页面
    result=Address.objects.get(pk=pk)
    return render(request,'Reception/users/user_address_modify.html',{'list':result})
def user_address_modify_han(request):
    #地址修改页面处理
    id=request.POST['id']
    username=request.POST['username']
    name=request.POST['name']
    phone=request.POST['phone']
    result=Address.objects.filter(address_id=id).update(address_name=name,address_username=username,address_phone=phone)
    if result:
        return HttpResponseRedirect('/user_address')
@show
def user_address_del(request,pk):
    #地址删除
    result=Address.objects.get(pk=pk)
    result.delete()
    return HttpResponseRedirect('/user_address')

@show
def user_address_add(request):
    #地址添加页面
    return render(request,'Reception/users/user_addres_add.html')
@show
def user_address_add_han(request):
    #地址添加处理
    # 地址添加
    if 'user' in request.session:
        name = request.POST['username']
        phone = request.POST['phone']
        address = request.POST['address']
        result = Address.objects.create(
            address_username=name,
            address_phone=phone,
            address_name=address,
            user_id=request.session['user_id']
        )
    return HttpResponseRedirect('/user_address')

@show
def user_core(request):
    #个人信息
    result=User.objects.get(pk=request.session['user_id'])
    return render(request,'Reception/users/user_core.html',{'list':result})
@show
def user_core_modify(request):
    #用户修改页面
    return render(request,'Reception/users/user_core_modify.html')
@show
def user_core_modify_han(request):
    #用户信息修改
    user_pic=request.FILES['pic']
    email=request.POST['email']
    sex=request.POST['sex']
    age=request.POST['age']
    text=request.POST['text']
    print(user_pic)
    set_path='%s/media/uploads/%s'%(settings.MEDIA_ROOT,user_pic.name)
    with open('set_path','wb') as f:
        for i in  user_pic.chunks():
            f.write(i)
    result=User.objects.filter(pk=request.session['user_id']).update(
        pic='media/uploads/%s'%user_pic.name,
        email=email,
        sex=sex,
        age=age,
        body=text
    )
    if result:
        del request.session['user_pic']
        request.session['request.session.user_pic']=str(User.objects.get(pk=request.session['user_id']).pic)
        return HttpResponseRedirect('/user_core')

@show
def user_comment(request,pk):
    #评价页面
    order = Oreder.objects.get(pk=pk)
    num=Order_page.objects.filter(order_id=pk)
    return render(request,'Reception/users/user_comment.html',{'list':order,'num':num})
@show
def user_comment_han(request):
    #评价内容处理
    text=request.POST.getlist('text','')
    comment_time=datetime.now()
    user_id = request.session['user_id']
    order_id=request.POST['id']
    new_state=Oreder.objects.filter(order_id=order_id).update(order_state=3)
    result=Order_page.objects.filter(order_id=order_id)
    for num,i in zip(text,result):
        new_result=User_comment.objects.create(goods_id=i.goods_id,user_id=user_id,manage_id=i.manage_id,comment_time=comment_time,comment_body=num,order_id=i.order_id,order_page_id=i.order_page_id)
    return HttpResponseRedirect('/user_order')
def user_order_logistics(request,pk):
    #物流信息
    result=Oreder.objects.get(order_id=pk)
    logistics=Logistics.objects.get(order=pk)
    address=Address.objects.get(pk=result.address_id)
    result_page=Order_page.objects.filter(order_id=pk)
    sum=Order_page.objects.filter(order_id=pk).aggregate(total=Sum('goods_sum'))
    return render(request,'Reception/users/user_order_logistics.html',{'list':result,'num':result_page,'logistics':logistics})
def user_comment_body(request,pk):
    #查看评论内容
    # sql='SELECT * FROM users_user_comment g LEFT JOIN order_order_page f on g.order_id=f.order_id GROUP BY g.user_comment_id having g.order_id='+str(pk)
    page=Order_page.objects.filter(order_id=pk)
    count=User_comment.objects.filter(order_id=pk)
    order=Oreder.objects.get(pk=pk)
    return render(request,'Reception/users/user_comment_body.html',{'num':page,'list':order,'count':count})

def user_activation(request):
    #邮箱激活发送
    user=User.objects.last()
    email=user.email
    username=user.username
    user_id=user.user_id
    time=datetime.now()
    path="会员"+username+'你好！尽快激活账号吧 <a href="http://127.0.0.1:8000/user_activation_han?id='+str(user_id)+'">点击激活用户</>'
    result=send_mail("欢迎您注册","",settings.EMAIL_FROM,[email],html_message=path,fail_silently=True)
    if result:
        User_email.objects.create(
            user_id=user_id,
            email_time=time,
            email_title='欢迎您注册',
            email_body='激活账号吧',
        )
        return HttpResponseRedirect('/user_activation_continue')
    return HttpResponse('失败')
def user_activation_continue(request):
    #激活页面
    return render(request,'Reception/email/email_activation.html')
def user_activation_han(request):
    #邮箱激活
    id=request.GET.get('id',1)
    result_new=User.objects.filter(pk=int(id)).update(state=1)
    if result_new:
        return HttpResponse('激活成功')
    else:
        return HttpResponse('激活失败')
def user_reactivation(request):
    #重新激活
    return render(request,'Reception/email/email_reactivation.html')
def user_colletion(request):
    #我的收藏
    num=[]
    list=[]
    result=User_collection.objects.filter(user_id=request.session['user_id'])
    for i in result:
        num.append(i.goods_id)
    for i in num:
        list.append(Manage_goods.objects.get(pk=i))
    return render(request,'Reception/users/user_collection.html',{'list':list})
def user_code(request):
    text=request.GET.get('text')
    if len(text)!=4:
        return HttpResponse(0)
    elif text.lower()!=request.session['Code'].lower():
        return HttpResponse(0)
    elif text.lower()==request.session['Code'].lower():
        return HttpResponse(1)