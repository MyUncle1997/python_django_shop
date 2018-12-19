from django.shortcuts import render
from .models import Manage,Manage_type,Manage_goods,Logistics,Manage_shop,Manage_role,Manage_power
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime
from shop1 import settings
from users.models import User_comment,User,User_email
import functools
import platform
import socket
import django
from django.db.models import Q,F
from django.core.mail import send_mail
from  order.models import Order_page,Oreder,Address
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from users.models import User
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
# Create your views here.

#修饰函数
def show(num):
    @functools.wraps(num)
    def run(request,*arg,**kw):
        if 'manage_user' in request.session:
            return num(request,*arg,**kw)
        else:
            return HttpResponseRedirect('/manage_login')
    return run
def manage_login(request):
    #后台登录页面
    return render(request, 'Backstage/login.html')
def manage_login_han(request):
    #登录跳转
    username=request.POST['username']
    password=request.POST['password']
    code = request.POST['code']
    Code = request.session['M_Code']
    result=Manage.objects.filter(manage_name=username,manage_pass=password)
    if code.lower()==Code.lower() and result:
        request.session['manage_user']=username
        request.session['manage_user_id']=Manage.objects.get(manage_name=username).manage_id
        manage = Manage.objects.get(pk=request.session['manage_user_id'])
        manage_role = manage.manage_role.power.all()
        url_list = []
        for i in manage_role:
            url_list.append(i.power_namespace + ':' + i.power_url)
        request.session['url_list']=url_list
        return HttpResponseRedirect('/manage_shop_home')
    elif code.lower()!=Code.lower() and result:
        return HttpResponse('验证码错误')
    else:
        return HttpResponse('用户或密码错误')

@show
def manage_shop_home(request):
    #店铺选择
    result=Manage_shop.objects.filter(manage_id=request.session['manage_user_id'])
    return render(request,'Backstage/shop/shop_list.html',{'list':result})
@show
def manage_home(request,pk):
    #主页
    request.session['shop_id'] = pk
    result=Manage_goods.objects.filter(shop_id=pk)
    sum=0
    for i in result:
        sum+=1
    #本机系统
    os=platform.platform()
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    Ed=django.VERSION
    #会员数
    num=set()
    num_new=Oreder.objects.filter(shop_id=request.session['shop_id'])
    for i in num_new:
        num.add(i.user_id)
    return render(request,'Backstage/users.html',{'len':sum,'os':os,'ip':ip,'Ed':Ed,'num':len(num)})
def manage_login_out(request):
    #退出登录
    try:
        del request.session['manage_user']
        del request.session['shop_id']
        return HttpResponseRedirect('/manage_login')
    except:
        return HttpResponseRedirect('/manage_login')
@show
def manage_add(request):
    #商品添加页面
    manage_user=Manage.objects.filter(manage_name=request.session['manage_user'])
    result = Manage_type.objects.filter(shop_id=request.session['shop_id']).order_by("-type_id")
    return render(request,'Backstage/goods/goods_add.html',{"list":result,'user':manage_user})
@show
def manage_add_han(request):
    #商品写入数据库
    set=Manage.objects.get(manage_name=request.session['manage_user'])
    goods_num=request.POST['goods_num']
    goods_name = request.POST['goods_name']
    goods_leibie = request.POST['goods_leibie']
    goods_oprice = request.POST['goods_oprice']
    goods_xprice = request.POST['goods_xprice']
    goods_count = request.POST['goods_count']
    goods_method = request.POST['goods_method']
    goods_infro = request.POST['goods_infro']
    goods_ishow = request.POST['goods_ishow']
    goods_address = request.POST['goods_address']
    goods_content = request.POST['goods_content']
    goods_user=set.manage_id
    goods_up_time =datetime.now()
    goods_pic = request.FILES['userfiles']
    set_path='%s/media/uploads/%s'% (settings.MEDIA_ROOT,goods_pic.name)
    with open(set_path,'wb') as f:
        for i in goods_pic.chunks():
            f.write(i)
    result=Manage_goods.objects.create(
        goods_num=goods_num,
        goods_name=goods_name,
        goods_oprice=goods_oprice,
        goods_xprice=goods_xprice,
        goods_count=goods_count,
        goods_method=goods_method,
        goods_infro=goods_infro,
        goods_ishow=goods_ishow,
        goods_pic='media/uploads/%s'% goods_pic.name,
        goods_address=goods_address,
        goods_body=goods_content,
        manager_id=goods_user,
        type_id=goods_leibie,
        up_time=goods_up_time,
        shop_id=request.session['shop_id'],
    )
    if result:
        return HttpResponseRedirect('/manage_add_list')
    else:
        return HttpResponse('失败')

@show
def manage_add_list(request):
    # 商品列表
    # result_type=Manage_type.objects.all()
    # print(result_type)
    result=Manage_goods.objects.filter(shop_id=request.session['shop_id'])
    paginator=Paginator(result,2)
    page = request.GET.get('page',1)
    gurrent=int(page)
    try:
        list=paginator.page(page)
    except PageNotAnInteger:
        list=paginator.page(1)
    except EmptyPage:
        list=paginator.page(paginator.num_pages)
    return render(request,'Backstage/goods/goods_add_list.html',locals())
@show
def manage_add_list_del(request,pk):
    #商品删除
    result=Manage_goods.objects.get(pk=pk)
    result.delete()
    if result:
        return HttpResponseRedirect('/manage_add_list')
    else:
        return HttpResponse('删除失败')
@show
def manage_add_list_modify(request,pk):
    #商品修改
    list = Manage_goods.objects.get(pk=pk)
    result = Manage_type.objects.order_by("-type_id")
    return render(request,'Backstage/goods/goods_add_modify.html',{'list':list,'list1':result})
@show
def manage_modify_han(request):
    #商品修改存储
    goods_num = request.POST['goods_num']
    goods_name = request.POST['goods_name']
    goods_leibie = request.POST['goods_leibie']
    goods_oprice = request.POST['goods_oprice']
    goods_xprice = request.POST['goods_xprice']
    goods_count = request.POST['goods_count']
    goods_method = request.POST['goods_method']
    goods_infro = request.POST['goods_infro']
    goods_ishow = request.POST['goods_ishow']
    goods_pic = request.FILES['userfiles']
    set_path='%s/media/uploads/%s'% (settings.MEDIA_ROOT,goods_pic.name)
    with open(set_path,'wb') as f:
        for i in goods_pic.chunks():
            f.write(i)
    goods_address = request.POST['goods_address']
    goods_content = request.POST['goods_content']
    id = request.POST['goods_id']
    goods_up_time = datetime.now()
    result=Manage_goods.objects.filter(pk=id).update(
        goods_num=goods_num,
        goods_name=goods_name,
        goods_oprice=goods_oprice,
        goods_xprice=goods_xprice,
        goods_count=goods_count,
        goods_method=goods_method,
        goods_infro=goods_infro,
        goods_ishow=goods_ishow,
        goods_pic='media/uploads/%s'% goods_pic.name,
        goods_address=goods_address,
        goods_body=goods_content,
        type_id=goods_leibie,
        up_time=goods_up_time,
    )
    if result:
        return HttpResponseRedirect('/manage_add_list')
    else:
        return HttpResponse('失败')
@show
def manage_add_up(reqeust,pk):
    #上架商品

    up_time=datetime.now()
    result=Manage_goods.objects.filter(pk=pk).update(goods_ishow=1,up_time=up_time)
    if result:
        return HttpResponseRedirect('/manage_add_list')
    else:
        return HttpResponse('上架失败')
@show
def manage_add_dowm(reqeust, pk):
    # 下架商品
    dowm_time = datetime.now()
    result = Manage_goods.objects.filter(pk=pk).update(goods_ishow=0,dowm_time=dowm_time)
    if result:
        return HttpResponseRedirect('/manage_add_list')
    else:
        return HttpResponse('下架失败')
@show
def manage_leibie(request):
    #商品类别添加页面
    return render(request,'Backstage/goods/goods_leibie.html')
@show
def manage_leibie_han(request):
    #类别添加处理
    name=request.POST['name']
    result=Manage_type.objects.create(type_name=name,shop_id=request.session['shop_id'])
    if result:
        return HttpResponseRedirect('/manage_leibie_list')
    else:
        return HttpResponse('添加失败')
@show
def manage_leibie_list(request):
    # 商品类别列表
    result=Manage_type.objects.filter(shop_id=request.session['shop_id']).order_by("-type_id")
    return render(request,'Backstage/goods/goods_leibie_list.html',{'list':result})
@show
def manage_leibie_del(request,pk):
    #商品类别删除
    result=Manage_type.objects.get(pk=pk)
    result.delete()
    return HttpResponseRedirect('/manage_leibie_list')
@show
def leibie_modify(request,pk):
    list = Manage_type.objects.get(pk=pk)
    return render(request,'Backstage/goods/goods_leibie_update.html',{"list":list})
@show
def leibie_modify_han(request):
    #商品类别修改
    name=request.POST['name']
    id=request.POST['id']
    result = Manage_type.objects.filter(pk=id).update(type_name=name)
    if result:
        return HttpResponseRedirect('/manage_leibie_list')
    else:
        return HttpResponse('失败')
@show
def manage_order_list(request):
    #商家订单列表
    num=[]
    order=[]
    # id=Manage.objects.get(manage_name=request.session['manage_user']).manage_id
    result=Order_page.objects.filter(shop_id=request.session['shop_id'])
    for i in  result:
        num.append(i.order_id)
    new_num=set(num)
    for i in new_num:
        new_order=Oreder.objects.get(pk=i)
        order.append(new_order)
    print(order)
    return  render(request,'Backstage/order/order_list.html',{'list':order})

@show
def manage_logistics(request,pk):
    #物流添加页面
    return render(request,'Backstage/order/manage_logistics.html',{'id':pk})
@show
def manage_logistics_han(request):
    #发货操作
    name=request.POST['name']
    num=request.POST['num']
    id=request.POST['id']

    user_id=Oreder.objects.get(pk=id).user_id
    print(user_id)
    time=datetime.now()
    result=Logistics.objects.create(logistics_name=name,logistics_num=num,user=user_id,order=id,logistics_time=time)
    result_order = Oreder.objects.filter(pk=id).update(order_state=1,send_time=time)
    if result and result_order:
        return  HttpResponseRedirect('/manage_order_list')
def manage_order_page(request,pk):
    #商家订单页面
    address_id=Oreder.objects.get(pk=pk).address_id
    page=Order_page.objects.filter(order_id=pk)
    address=Address.objects.get(pk=address_id)
    order=Oreder.objects.get(pk=pk)
    user=order.user_id
    name=User.objects.get(pk=user)
    return render(request,'Backstage/order/manage_order_page.html',{'address':address,'num':page,'list':order,'name':name})
def manage_order_comment(request,pk):
    #商家查看评论内容
    # sql='SELECT * FROM users_user_comment g LEFT JOIN order_order_page f on g.order_id=f.order_id GROUP BY g.user_comment_id having g.order_id='+str(pk)
    page=Order_page.objects.filter(order_id=pk)
    count=User_comment.objects.filter(order_id=pk)
    order=Oreder.objects.get(pk=pk)
    return render(request,'Backstage/order/order_comment.html',{'num':page,'list':order,'count':count})
def manage_member_list(request):
    #店铺用户会员
    num=set()
    sum=[]
    result=Oreder.objects.filter(shop_id=request.session['shop_id'])
    for i in result:
        num.add(i.user_id)
    for i in num:
        sum.append(User.objects.get(pk=i))
    return render(request,'Backstage/member/member_list.html',{'sum':sum})
def manage_member_email(request,pk):
    #会员邮件发送页面
    # email=User.objects.get(pk=pk).email
    # print(email)
    return render(request,'Backstage/member/member_email_send.html',{'id':pk})
def manage_member_han(request):
    #邮箱发送处理
    id=request.POST['id']
    result_user=User.objects.get(pk=id)
    email=result_user.email
    text=request.POST['text']
    header=request.POST['header']
    result=send_mail(header, "", settings.EMAIL_FROM, [email], html_message=text, fail_silently=True)
    if result:
        User_email.objects.create(email_time=datetime.now(),email_body=text,email_title=header,user_id=id)
        return HttpResponse('发送成功')
    return HttpResponse('发送失败')
def manage_show_email(request,pk):
    #邮箱列表
    result=User_email.objects.filter(user_id=pk)
    return render(request,'Backstage/member/member_email_list.html',{'sum':result})
def manage_power_list(request):
    #权限列表
    if request.method=='POST':
        name=request.POST['name']
        url = request.POST['url']
        url_name = request.POST['url_name']
        q1=Q()
        q1.connector='and'
        if name!='':
            q1.children.append(('power_name',name))
        if url != '':
            q1.children.append(('power_name', name))
        if url_name != '':
            q1.children.append(('power_name', name))
        result = Manage_power.objects.filter(q1)
        paginator = Paginator(result, 2)
        page = request.GET.get('page', 1)
        gurrent = int(page)
        try:
            list = paginator.page(page)
        except PageNotAnInteger:
            list = paginator.page(1)
        except EmptyPage:
            list = paginator.page(paginator.num_pages)
        return render(request, 'Backstage/power/power_list.html', locals())
    else:
        result=Manage_power.objects.all()
        paginator = Paginator(result, 2)
        page = request.GET.get('page', 1)
        gurrent = int(page)
        try:
            list = paginator.page(page)
        except PageNotAnInteger:
            list = paginator.page(1)
        except EmptyPage:
            list = paginator.page(paginator.num_pages)
        return render(request,'Backstage/power/power_list.html',locals())
def manage_power_add(request):
    #权限添加
    return render(request,'Backstage/power/power_add.html')
def manage_power_han(request):
    #权限添加处理
    try:
        name=request.POST['name']
        url=request.POST['url']
        power_namespace=request.POST['namespace']
        result=Manage_power.objects.create(power_name=name,power_url=url,power_namespace=power_namespace)
        if result:
            return HttpResponse(1)
    except:
        return HttpResponse(0)
def manage_power_modify(request,pk):
    #权限编辑
    list=Manage_power.objects.get(pk=pk)
    return render(request,'Backstage/power/power_modify.html',{'list':list})
def manage_power_modify_han(request):
    #权限编辑处理
    try:
        id=request.POST['id']
        name=request.POST['name']
        url=request.POST['url']
        namespace=request.POST['namespace']
        result=Manage_power.objects.filter(pk=id).update(power_name=name,power_url=url,power_namespace=namespace)
        if result:
            return HttpResponse(1)
    except:
        return HttpResponse(0)

def manage_power_del(requst):
    #权限删除
    try:
        id=requst.GET.get('num')
        result=Manage_power.objects.get(pk=id)
        result.delete()
        return HttpResponse(1)
    except:
        return HttpResponse(0)
def manage_role_list(request):
    #角色列表
    if request.method=='POST':
        name=request.POST['name']
        q1=Q()
        if name!='':
            q1.children.append(('role_name',name))
        result = Manage_role.objects.filter(q1)
        paginator = Paginator(result, 2)
        page = request.GET.get('page', 1)
        gurrent = int(page)
        try:
            list = paginator.page(page)
        except PageNotAnInteger:
            list = paginator.page(1)
        except EmptyPage:
            list = paginator.page(paginator.num_pages)
        return render(request, 'Backstage/power/role_list.html', locals())
    else:
        result=Manage_role.objects.order_by('id')
        paginator = Paginator(result, 2)
        page = request.GET.get('page', 1)
        gurrent = int(page)
        try:
            list = paginator.page(page)
        except PageNotAnInteger:
            list = paginator.page(1)
        except EmptyPage:
            list = paginator.page(paginator.num_pages)
        return render(request,'Backstage/power/role_list.html',locals())
def manage_role_add(request):
    #角色添加
    if request.method=='POST':
        try:
            id_list=request.POST.getlist('id')
            name = request.POST['name']
            role=Manage_role()
            role.role_name=name
            role.add_user=request.session.get('manage_user')
            role.status=1
            role.add_time=datetime.now()
            role.save()
            result=Manage_role.objects.all().last()
            result.power.set(id_list)
            result.save()
            # result = Manage_role.objects.create(role_name=name, add_user=request.session.get('manage_user'),status=1)
            return HttpResponse(1)
        except:
            return HttpResponse(0)
    else:
        list=Manage_power.objects.all()
        return render(request,'Backstage/power/role_add.html',locals())
def manage_role_modify(request):
    #角色编辑
    if request.method=='POST':
        try:
            id_list=request.POST.getlist('list_id')
            name = request.POST['name']
            id = request.POST['id']
            role=Manage_role.objects.filter(id=id).update(role_name=name)
            result=Manage_role.objects.filter(id=id).first()
            result.power.set(id_list)
            result.save()
            # result = Manage_role.objects.create(role_name=name, add_user=request.session.get('manage_user'),status=1)
            return HttpResponse(1)
        except:
            return HttpResponse(0)
    else:
        id=request.GET.get('id')
        num=[]
        one=Manage_role.objects.filter(id=id).first()
        ret=one.power.all()
        for i in ret:
            num.append(i.id)
        list = Manage_power.objects.all()
        return render(request,'Backstage/power/role_modify.html',locals())
def manage_role_del(request):
    #角色删除
    try:
        id=request.GET.get('num')
        result=Manage_role.objects.get(pk=id)
        result.delete()
        return HttpResponse(1)
    except:
        return HttpResponse(0)