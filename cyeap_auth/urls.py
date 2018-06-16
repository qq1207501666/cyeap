"""
自己创建的urls文件
"""

from django.conf.urls import url
from cyeap_auth import views

urlpatterns = [
    url(r'^login/', views.login),  # 登录
    url(r'^logout/', views.logout),  # 登出
    url(r'^login_auth/', views.login_auth),  # 登录验证
]
