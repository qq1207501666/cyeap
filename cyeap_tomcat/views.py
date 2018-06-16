from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from cyeap_tomcat import models

from django.forms.models import model_to_dict  # 对象转换成字典
from cyeap.utils import page_util
from django.utils.safestring import mark_safe  # 防止html代码直接红果果的显示在页面上
import json


# Create your views here.

@login_required  # 要求必须登录状态
def index(request):
    """
    Tomcat部署管理首页
    :param request:
    :return: 首页
    """
    return render(request, "cyeap_tomcat/index.html")


@login_required  # 要求必须登录状态
def get_tomcat_server(request):
    """
    Ajax 获取页面数据
    :param request:
    :return:
    """
    params = request.GET.get("params")  # 获取请求参数
    params = json.loads(params)  # 解析json数据
    page_num = params.get("page_num")
    page_num = page_num if page_num else 1
    page_size = params.get("page_size")
    page_size = page_size if page_size else 100
    # ---- 获取查询条件 ---- #
    tomcat_name = params.get("tomcat_name")
    tomcat_name = tomcat_name if tomcat_name else ""
    tomcat_alias = params.get("tomcat_alias")
    tomcat_alias = tomcat_alias if tomcat_alias else ""
    ip4_inner = params.get("ip4_inner")
    ip4_inner = ip4_inner if ip4_inner else ""
    webapp_name = params.get("webapp_name")
    webapp_name = webapp_name if webapp_name else ""

    print("%s %s %s %s" % (tomcat_name, tomcat_alias, ip4_inner, webapp_name))
    # ---------------------- #
    record_count = models.TomcatServer.objects.filter(name__contains=tomcat_name, alias__contains=tomcat_alias,
                                                      ip4_inner__contains=ip4_inner,
                                                      webapp__name__contains=webapp_name).count()  # 总记录数
    json_dict = {}
    if record_count > 0:
        page_num = page_util.revise_page_num(page_num, page_size, record_count)  # 修正页码
        start = (page_num - 1) * page_size  # 取记录的开始下标(含)
        end = page_num * page_size  # 取记录的开始下标(不含)
        tomcat_servers = models.TomcatServer.objects.filter(name__contains=tomcat_name, alias__contains=tomcat_alias,
                                                            ip4_inner__contains=ip4_inner,
                                                            webapp__name__contains=webapp_name)[
                         start: end]  # 分页数据利用QuerySets的惰性进行分页,提高效率
        for server in tomcat_servers:
            dt = model_to_dict(server)
            dt["webapp_deploy_path"] = server.webapp.deploy_path
            json_dict[str(server.id)] = dt
    html = page_util.page_html(page_num, page_size, record_count)
    json_dict["page_html"] = mark_safe(html)
    return JsonResponse(json_dict)
