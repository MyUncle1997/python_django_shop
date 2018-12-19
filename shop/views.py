from django.shortcuts import render
import functools
from manageuser.models import Manage,Manage_shop,Manage_goods,Manage_type
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime
from shop1 import settings
# Create your views here.

def show(num):
    @functools.wraps(num)
    def run(request,*arg,**kw):
        if 'manage_user' in request.session:
            return num(request,*arg,**kw)
        else:
            return HttpResponseRedirect('/login')
    return run
def shop_open(request):
    #开店页面
    return render(request,'Backstage/shop/shop_open.html')
def shop_open_han(request):
    #开店数据处理
    username=request.POST['username']
    print(username)
    password = request.POST['password']
    shop_name = request.POST['shop_name']
    shop_username = request.POST['shop_username']
    shop_address = request.POST['shop_address']
    shop_img = request.FILES['shop_img']
    str_img='%s/media/uploads/%s'%(settings.MEDIA_ROOT,shop_img.name)
    with open(str_img,'wb') as f:
        for i in shop_img.chunks():
            f.write(i)
    manage_result=Manage.objects.create(manage_name=username,manage_pass=password)
    manage=Manage.objects.last().manage_id
    shop_result=Manage_shop.objects.create(
        manage_shop_name=shop_name,
        manage_shop_address=shop_address,
        manage_id=manage,
        manage_shop_time=datetime.now(),
        manage_shop_username=shop_username,
        manage_shop_pic='media/uploads/%s'%(shop_img.name),
    )
    return HttpResponseRedirect('/manage_login')
@show
def shop_add(request):
    #商家店铺添加
    return render(request,'Backstage/shop/shop_open_add.html')
@show
def shop_add_han(request):
    # 开店添加数据处理
    manage = Manage.objects.get(manage_name=request.session['manage_user']).manage_id
    add=Manage_shop.objects.filter(manage_id=manage).count()
    print(add)
    if add>5:
        return HttpResponse('你开的店铺超出数量，请联系客服处理')
    else:
        shop_name = request.POST['shop_name']
        shop_username = request.POST['shop_username']
        shop_address = request.POST['shop_address']
        shop_img = request.FILES['shop_img']
        str_img = '%s/media/uploads/%s' % (settings.MEDIA_ROOT, shop_img.name)
        with open(str_img, 'wb') as f:
            for i in shop_img.chunks():
                f.write(i)
        shop_result = Manage_shop.objects.create(
            manage_shop_name=shop_name,
            manage_shop_address=shop_address,
            manage_id=manage,
            manage_shop_time=datetime.now(),
            manage_shop_username=shop_username,
            manage_shop_pic='media/uploads/%s' % (shop_img.name),
        )
        return HttpResponseRedirect('/manage_shop_home')
def shop_list(request):
    #店铺显示
    result=Manage_shop.objects.all()
    return render(request,'Reception/shop/shop_list.html',{'list':result})
def shop_list_home(request,pk):
    #店铺类别
    result_goods=Manage_goods.objects.filter(shop_id=pk)
    result_type=Manage_type.objects.filter(shop_id=pk)
    return render(request,'Reception/shop/shop_list_home.html',{'list':result_type,'goods':result_goods})
def shop_home_content(request,pk,gk):
    #店铺商品分类
    result_goods=Manage_goods.objects.filter(shop_id=pk,type_id=gk)
    result_type=Manage_type.objects.filter(shop_id=pk)
    return render(request,'Reception/shop/shop_list_home.html',{'list':result_type,'goods':result_goods})