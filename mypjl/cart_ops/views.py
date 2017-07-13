# coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
# from django.db.models import Sum
from models import *
from user_ops.login_decrator import user_islogin
# Create your views here.


def add(request):
    try:
        uid = request.session.get('uid')
        gid = int(request.GET.get('gid'))
        count = int(request.GET.get('count', '1'))

        cart = CartInfo.objects.filter(user_id=uid, goods_id=gid)
        if len(cart) == 1:  # 如果用户uid已经购买了商品gid，则将数量+count
            cart1=cart[0]
            cart1.count+=count
            cart1.save()
        else:  # 用户uid没有购买gid过商品则添加
            cart=CartInfo()
            cart.user_id=uid
            cart.goods_id=gid
            cart.count=count
            cart.save()
        return JsonResponse({'isadd':1})
    except:
        return JsonResponse({'isadd':0})


def count(request):
    uid = int(request.session.get('uid'))
    count1 = CartInfo.objects.filter(user_id=uid).count()#10
    # count1=CartInfo.objects.filter(user_id=uid).aggregate(Sum('count')).get('count__sum')#字典
    return JsonResponse({'count': count1})


@user_islogin
def index(request):
    uid=int(request.session.get('uid'))
    cart_list=CartInfo.objects.filter(user_id=uid)
    context={'wtitle': '购物车', 'cart_list': cart_list}
    return render(request, 'cart_ops/cart.html', context)

