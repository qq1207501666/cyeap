"""
自己创建的urls文件
"""

from django.conf.urls import url
from cyeap_tomcat import views

urlpatterns = [
    url(r'^index/', views.index),  # 首页
    url(r'^get_tomcat_server/', views.get_tomcat_server),  # 获取表格数据
    url(r'^upgrade_webapp/', views.upgrade_webapp),  # 升级项目
]
