"""
自己创建的urls文件
"""

from django.conf.urls import url, include    # 导入url, include
from demo import views

urlpatterns = [
    url(r'^hello/', views.hello_world),
    url(r'^get_student/', views.get_student),
    url(r'^login/', views.login),
]
