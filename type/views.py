from django.shortcuts import render
from manageuser.models import Manage_type,Manage_goods,Manage
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
import functools
# Create your views here.
def type_home(request):
    list1=Manage_type.objects.order_by()
    id=Manage_type.objects.all().first().type_id
    # sql="SELECT * FROM manageuser_manage_type g INNER JOIN manageuser_manage_goods f on g.type_id=f.type_id where g.type_id="+str(id)
    goods=Manage_goods.objects.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(goods,4)
    count1 = int(page)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request,'Reception/type/type_home.html',locals())

def type_home_content(request,pk):
    list1 = Manage_type.objects.order_by()
    goods=Manage_goods.objects.filter(type_id=pk)
    page = request.GET.get("page", 1)
    paginator = Paginator(goods, 4)
    count1 = int(page)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request,'Reception/type/type_content.html',locals())