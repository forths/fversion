# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from hashlib import sha1
from models import *
from django.http import JsonResponse
import datetime
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

    # 如果没有查到数据则返回[]，如果查到数据则返回[UserInfo]
    result = UserInfo.objects.filter(uname=uname)

    if len(result) == 0:
        # 用户名不存在
        return render(request, 'user_ops/login.html', context)
    else:
        upwd = post.get('pwd')
        s1 = sha1()
        s1.update(upwd)
        upwd_sha1 = s1.hexdigest()
        if result[0].upwd == upwd_sha1:
            # 登录成功
            response = redirect(request.session.get('url_path', '/user/userinfo'))
            request.session['uid'] = result[0].id
            # 记住用户名
            if ujz == '1':
                response.set_cookie('uname', uname, expires=datetime.datetime.now() + datetime.timedelta(days=14))
            else:
                response.set_cookie('uname', '', max_age=-1)
            return response
        else:
            # 密码错误
            context['error_p'] = '密码错误'
            return render(request, 'user_ops/login.html', context)


def userinfo(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    context = {'user': user}
    return render(request, 'user_ops/userinfo.html', context)
