from django.shortcuts import render
from django.http import HttpResponse
from manageuser.models import Manage_goods
from order.models import Order_page,Oreder
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from users.models import User
# Create your views here.
def index(request):
    result=Manage_goods.objects.order_by('goods_id')
    page = request.GET.get("page", 1)
    paginator=Paginator(result,4)
    count1=int(page)
    try:
        list=paginator.page(page)
    except PageNotAnInteger:
        list=paginator.page(1)
    except EmptyPage:
        list=paginator.page(paginator.num_pages)
    # pic = User.objects.get(username=request.session['user']).pic
    # img=str(pic)
    # print(img)
    sql='SELECT COUNT(goods_id) num,goods_id,g.order_id FROM order_oreder g INNER JOIN order_order_page f on g.order_id=f.order_id GROUP BY f.goods_id'
    count=Oreder.objects.raw(sql)
    return render(request, 'Reception/goods/index.html',locals())



def goods_search(request):
    text=request.POST['text']
    num=[]
    sum=[]
    result=Manage_goods.objects.all()
    for i in result:
        if i.goods_name in text or text in i.goods_name:
            num.append(i.goods_id)
    for i in num:
        sum.append(Manage_goods.objects.get(pk=i))
    sql='SELECT COUNT(goods_id) num,goods_id,g.order_id FROM order_oreder g INNER JOIN order_order_page f on g.order_id=f.order_id GROUP BY f.goods_id'
    count=Oreder.objects.raw(sql)
    return render(request, 'Reception/goods/goods_search.html',{'list':sum,'count':count})