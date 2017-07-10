# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from hashlib import sha1
from models import *
from django.http import JsonResponse
import datetime
import login_decrator
# Create your views here.


def register(request):
    context = {'wtitle': '天天生鲜-注册', 'top': '0'}
    return render(request, 'user_ops/register.html', context)


def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get("pwd")
    uemail = post.get('email')
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    u = UserInfo()
    u.uname = uname
    u.upwd = upwd_sha1
    u.uemail = uemail
    u.save()
    return redirect('/user/login/')


def register_valid(request):
    # 接收用户名
    uname = request.GET.get('uname')
    # 查询当前用户的个数
    data = UserInfo.objects.filter(uname=uname).count()

    # 返回json{'valid':1或0}
    context = {'valid': data}
    return JsonResponse(context)


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'wtitle': '登录', 'uname': uname, 'top': '0'}
    return render(request, 'user_ops/login.html', context)


def login_handle(request):
    post = request.POST
    uname = post.get('username')
    ujz = post.get('user_jz', 0)
    context = {'wtitle': '登录', 'uname': uname, 'top': '0'}
    result = UserInfo.objects.filter(uname=uname)
    upwd = post.get('pwd')
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    if result[0].upwd == upwd_sha1:
        # 登录成功
        response = redirect(request.session.get('url_path', '/'))

        request.session['uid'] = result[0].id
        request.session['uname'] = result[0].uname
        # 记住用户名
        if ujz == 'on':
            response.set_cookie('uname', uname, expires=datetime.datetime.now() + datetime.timedelta(days=14))
        else:
            response.set_cookie('uname', '', max_age=-1)
        return response
    else:
        # 密码错误
        context['error_p'] = '密码错误'
        print context['error_p']
        return render(request, 'user_ops/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/user/login/')


@login_decrator.user_islogin
def userinfo(request):
    user = UserInfo.objects.get(pk=request.session['uid'])

    context = {'user': user, 'wtitle': '个人信息'}
    return render(request, 'user_ops/userinfo.html', context)


@login_decrator.user_islogin
def user_center_order(request):
    context = {'wtitle': '全部订单'}
    return render(request, 'user_ops/user_center_order.html', context)


@login_decrator.user_islogin
def user_center_site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method == 'POST':
        post = request.POST
        ushou = post.get('ushou')
        uaddress = post.get('uaddress')
        ucode = post.get('ucode')
        uphone = post.get('uphone')

        user.ushou = ushou
        user.uaddress = uaddress
        user.ucode = ucode
        user.uphone = uphone
        user.save()
    context = {'user': user, 'wtitle': '收货地址'}
    return render(request, 'user_ops/user_center_site.html', context)
