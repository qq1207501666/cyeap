from apscheduler.schedulers.background import BackgroundScheduler
from cyeap_tomcat import models
from cyeap.utils import mq_util
import logging

logger = logging.getLogger('django')  # 获取日志对象


def update_tomcat_state():
    """
    检查更新Tomcat状态,作为一个job被定时调度
    :return:
    """
    tomcat_servers = models.TomcatServer.objects.all()
    for tomcat_server in tomcat_servers:
        cmd = {"cmd": "check_tomcat",
               "args": {"tomcat_path": tomcat_server.deploy_path, }
               }
        try:
            logger.error("Tomcat定时巡检[%s]" % tomcat_server.ip4_inner)
            result = mq_util.call(tomcat_server.ip4_inner, cmd)  # 向agent发送命令
            logger.error("Tomcat定时巡检结果-----[%s]" % result)
        except Exception as ex:
            result = 4
            logger.error("Tomcat定时巡检结果4444444444444%s" % str(ex))
        if result == "True":
            result = 1
            logger.error("Tomcat定时巡检结果1111111111111%s" % tomcat_server.state)
        if result == "False":
            result = 2
            logger.error("Tomcat定时巡检结果1111111111111%s" % tomcat_server.state)
        if result != tomcat_server.state:  # 状态不一致则需要更新数据库中的状态
            logger.error("Tomcat修改咯%s%s" % (tomcat_server.state, result))
            tomcat_server.state = result
            tomcat_server.save()


def start():
    # 定时任务启动
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_tomcat_state, trigger='interval', seconds=30)  # 每60秒检查更新一次Tomcat状态
    scheduler.start()
