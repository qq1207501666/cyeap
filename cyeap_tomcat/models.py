from django.db import models


# Create your models here.


class TomcatWebapp(models.Model):
    """
        应用程序表
    """
    id = models.AutoField(primary_key=True, verbose_name="项目编号")
    alias = models.CharField(max_length=128, null=True, blank=True, verbose_name="项目中文别名")
    deploy_path = models.CharField(max_length=128, verbose_name="项目部署路径", default="/local/webapp/")
    source_path = models.CharField(max_length=128, verbose_name="源路径")
    current_version = models.CharField(max_length=128, null=True, blank=True, verbose_name="项目版本")  # 项目版本
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")  # 创建时间
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")  # 更新时间
    remark = models.CharField(max_length=512, null=True, blank=True, verbose_name="备注", default="")  # 备注

    def __str__(self):
        return "%s  %s" % (self.alias, self.deploy_path)

    class Meta:
        db_table = "tomcat_webapp"


class TomcatServer(models.Model):
    """
        Tomcat服务表
    """
    id = models.AutoField(primary_key=True, verbose_name="Tomcat服务编号")
    alias = models.CharField(max_length=128, null=True, blank=True, verbose_name="Tomcat中文别名")
    deploy_path = models.CharField(max_length=128, verbose_name="Tomcat部署路径", default="/local/server/")
    version = models.CharField(max_length=128, null=True, blank=True, verbose_name="Tomcat版本")
    ip4_inner = models.CharField(max_length=32, null=True, blank=True, verbose_name="内网IP_v4")
    ip4_outer = models.CharField(max_length=32, null=True, blank=True, verbose_name="外网IP_v4")
    http_port = models.SmallIntegerField(verbose_name="HTTP端口")
    shutdown_port = models.SmallIntegerField(verbose_name="SHUTDOWN端口")
    ajp_port = models.SmallIntegerField(verbose_name="AJP端口")
    state = models.SmallIntegerField(verbose_name="运行状态")  # 1 运行中  2 已停止  4 未知
    config = models.TextField(null=True, blank=True, verbose_name="配置文件")
    webapp = models.ForeignKey(TomcatWebapp, on_delete=models.CASCADE, verbose_name="部署应用")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    remark = models.CharField(max_length=512, null=True, blank=True, verbose_name="备注", default="")

    def __str__(self):
        return "%s  %s" % (self.alias, self.deploy_path)

    class Meta:
        db_table = "tomcat_server"


class TomcatServerRecord(models.Model):
    """
    TomcatServer的操作记录
    """
    username = models.CharField(max_length=16)  # 操作人的用户名
    RECORD_TYPE = (
        (1, "启动"),
        (2, "停止"),
        (3, "重启"),
        (4, "升级"),
        (5, "回滚"),
    )
    record_type = models.SmallIntegerField(choices=RECORD_TYPE)  # 记录类型
    summary = models.CharField(max_length=256)  # 摘要
    detail = models.TextField(null=True, blank=True)  # 详情
    create_time = models.DateTimeField(auto_now=True)  # 创建时间
    tomcat_server = models.ForeignKey(TomcatServer, on_delete=models.CASCADE)  # 关联的tomcat server

    class Meta:
        db_table = "tomcat_server_record"
