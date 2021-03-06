from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict  # 对象转换成字典
from django.utils.safestring import mark_safe  # 防止html代码直接红果果的显示在页面上
import json
import logging
from cyeap.utils import page_util, str_util, socket_util, mq_util
from cyeap_tomcat import models, timing

logger = logging.getLogger('django')  # 获取日志对象
timing.start()  # 启动定时任务


@login_required  # 要求必须登录状态
def index(request):
    """
    Tomcat部署管理首页
    :param request:
    :return: 首页
    """
    return render(request, "cyeap_tomcat/index.html")


@login_required
def restart_tomcat(request):
    params = request.POST.get("params")  # 获取请求参数
    params = json.loads(params)  # 解析json数据
    logger.error("请求参数:%s" % params)
    tomcat_ids = str_util.none2empty(params.get("tomcat_ids"))  # TomcatID列表
    opt = str_util.none2empty(params.get("opt"))  # 要进行的操作 启动|停止|重启
    json_dict = {}
    for tomcat_id in tomcat_ids:
        tomcat_server = models.TomcatServer.objects.get(id=tomcat_id)  # 获取要升级的TomcatServer
        cmd = {"cmd": "restart_tomcat",
               "args": {"opt": opt,
                        "tomcat_path": tomcat_server.deploy_path, }
               }
        logger.error("向%s发送命令: %s" % (tomcat_server.ip4_inner, cmd))
        try:
            result = mq_util.call(tomcat_server.ip4_inner, cmd)  # 向agent发送命令
            record = models.TomcatServerRecord()
            record.username = request.user.username  # 获取当前登录的用户名
            record.tomcat_server = tomcat_server
            if opt == "start":
                record.record_type = 1
                record.summary = "启动Tomcat服务"
            elif opt == "stop":
                record.record_type = 2
                record.summary = "停止Tomcat服务"
            elif opt == "restart":
                record.record_type = 3
                record.summary = "重启Tomcat服务"
            if record:
                record.save()  # 保存操作记录
        except Exception as ex:
            result = str(ex)
        logger.error("命令发送结果: %s" % result)
        if result == "START OK":
            tomcat_server.state = 1
        elif result == "STOP OK":
            tomcat_server.state = 2
        else:
            tomcat_server.state = 4
        tomcat_server.save()  # 保存Tomcat服务状态更改
        print(type(result))
        result = result.replace("\n", "</br>")  # 将 \n 替换成html的换行符</br>
        json_dict = {str(tomcat_server.ip4_inner): mark_safe(result)}
    return JsonResponse(json_dict)


@login_required  # 要求必须登录状态
def get_tomcat_server(request):
    """
    Ajax 获取页面数据
    :param request:
    :return:
    """

    params = request.GET.get("params")  # 获取请求参数
    params = json.loads(params)  # 解析json数据
    logger.error("请求参数:%s" % params)
    # ---- 获取查询条件 ---- #
    page_num = params.get("page_num")
    page_num = page_num if page_num else 1
    page_size = params.get("page_size")
    page_size = page_size if page_size else 100
    tomcat_name = str_util.none2empty(params.get("tomcat_name"))
    webapp_name = str_util.none2empty(params.get("webapp_name"))
    tomcat_alias = str_util.none2empty(params.get("tomcat_alias"))
    ip4_inner = str_util.none2empty(params.get("ip4_inner"))
    # ---------------------- #
    json_dict = {}  # 响应的json数据字典
    record_count = models.TomcatServer.objects.filter(deploy_path__contains=tomcat_name,
                                                      webapp__deploy_path__contains=webapp_name,
                                                      alias__contains=tomcat_alias,
                                                      ip4_inner__contains=ip4_inner,
                                                      ).count()  # 总记录数
    if record_count > 0:
        page_num = page_util.revise_page_num(page_num, page_size, record_count)  # 修正页码
        start = (page_num - 1) * page_size  # 取记录的开始下标(含)
        end = page_num * page_size  # 取记录的开始下标(不含)
        tomcat_servers = models.TomcatServer.objects.filter(deploy_path__contains=tomcat_name,
                                                            webapp__deploy_path__contains=webapp_name,
                                                            alias__contains=tomcat_alias,
                                                            ip4_inner__contains=ip4_inner, )[
                         start: end]  # 分页数据利用QuerySets的惰性进行分页查询,提高效率
        for server in tomcat_servers:
            dt = model_to_dict(server)
            dt["webapp_deploy_path"] = server.webapp.deploy_path  # 将关联表的数据查出加入到json数据字典中
            json_dict[str(server.id)] = dt  # 多条数据,每条以ID为key组成的字典
        html = page_util.page_html(page_num, page_size, record_count)  # 获取分页html
        json_dict["page_html"] = mark_safe(html)
    else:
        json_dict["page_html"] = ""
    return JsonResponse(json_dict)


def upgrade_webapp(request):
    """
    升级项目
    :param request:
    :return:
    """
    params = request.POST.get("params")  # 获取请求参数
    params = json.loads(params)  # 解析json数据
    logger.error("请求参数:%s" % params)
    tomcat_ids = str_util.none2empty(params.get("tomcat_ids"))  # TomcatID列表
    summary = str_util.none2empty(params.get("summary"))  # 升级摘要
    revision = str_util.none2empty(params.get("revision"))  # 更新至版本
    json_dict = {}
    for tomcat_id in tomcat_ids:
        tomcat_server = models.TomcatServer.objects.get(id=tomcat_id)  # 获取要升级的TomcatServer
        cmd = {"cmd": "upgrade",
               "args": {"webapp_path": tomcat_server.webapp.deploy_path,
                        "tomcat_path": tomcat_server.deploy_path,
                        "revision": revision}
               }
        logger.error("向%s发送命令: %s" % (tomcat_server.ip4_inner, cmd))
        try:
            result = mq_util.call(tomcat_server.ip4_inner, cmd)  # 向agent发送命令
            record = models.TomcatServerRecord()
            record.username = request.user.username  # 获取当前登录的用户名
            record.summary = summary
            record.detail = result  # 将返回结果作为详情保存
            record.tomcat_server = tomcat_server
            if not revision:  # 没有指定版本号,插入TomcatServer操作记录: 升级
                record.record_type = 4  # 类型 4 为升级
            elif revision:  # 有版本号,插入TomcatServer操作记录: 回滚
                record.record_type = 5  # 类型 5 为回滚
            if record:
                record.save()
        except Exception as ex:
            result = str(ex)
        logger.error("命令发送结果: %s" % result)
        result = result.replace("\n", "</br>")  # 将 \n 替换成html的换行符</br>
        json_dict = {str(tomcat_server.ip4_inner): mark_safe(result)}
    return JsonResponse(json_dict)
