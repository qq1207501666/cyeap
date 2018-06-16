from django.shortcuts import render, HttpResponse, redirect
import django.contrib.auth as dj_auth


# Create your views here.


def login(request):
    """
    登录
    :param request:
    :return: 登录页面
    """
    return render(request, "cyeap_auth/login.html")


def login_auth(request):
    """
    登录验证
    :param request:
    :return:
    """
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = dj_auth.authenticate(username=username, password=password)
    if user:
        dj_auth.login(request, user)  # 用户登录
        return redirect("/cyeap_tomcat/index/")
    else:
        error = "用户名或密码错误!"
        return render(request, "cyeap_auth/login.html", {"error": error})


def logout(request):
    """
    登出
    :param request:
    :return: 退出登录
    """
    dj_auth.logout(request)
    return redirect("/cyeap_tomcat/index/")
