from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import JsonResponse
from cyeap_tomcat import models

from django.forms.models import model_to_dict  # 对象转换成字典
from cyeap.utils import page_util, str_util
from django.utils.safestring import mark_safe  # 防止html代码直接红果果的显示在页面上
import json
import logging

logger = logging.getLogger('django')  # 获取日志对象


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
    # ---- 获取查询条件 ---- #
    page_num = params.get("page_num")
    page_num = page_num if page_num else 1
    page_size = params.get("page_size")
    page_size = page_size if page_size else 100
    tomcat_name = str_util.none2empty(params.get("tomcat_name"))
    tomcat_alias = str_util.none2empty(params.get("tomcat_alias"))
    ip4_inner = str_util.none2empty(params.get("ip4_inner"))
    webapp_name = str_util.none2empty(params.get("webapp_name"))
    logger.error("请求参数:%s" % params)
    # ---------------------- #
    json_dict = {}  # 响应的json数据字典
    record_count = models.TomcatServer.objects.filter(name__contains=tomcat_name, alias__contains=tomcat_alias,
                                                      ip4_inner__contains=ip4_inner,
                                                      webapp__name__contains=webapp_name).count()  # 总记录数
    if record_count > 0:
        page_num = page_util.revise_page_num(page_num, page_size, record_count)  # 修正页码
        start = (page_num - 1) * page_size  # 取记录的开始下标(含)
        end = page_num * page_size  # 取记录的开始下标(不含)
        tomcat_servers = models.TomcatServer.objects.filter(name__contains=tomcat_name, alias__contains=tomcat_alias,
                                                            ip4_inner__contains=ip4_inner,
                                                            webapp__name__contains=webapp_name)[
                         start: end]  # 分页数据利用QuerySets的惰性进行分页查询,提高效率
        for server in tomcat_servers:
            dt = model_to_dict(server)
            dt["webapp_deploy_path"] = server.webapp.deploy_path  # 将关联表的数据查出加入到json数据字典中
            json_dict[str(server.id)] = dt  # 多条数据,每条以ID为key组成的字典
    html = page_util.page_html(page_num, page_size, record_count)  # 获取分页html
    json_dict["page_html"] = mark_safe(html)
    return JsonResponse(json_dict)
