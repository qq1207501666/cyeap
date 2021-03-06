# Generated by Django 2.0.3 on 2018-07-06 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TomcatServer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Tomcat服务编号')),
                ('alias', models.CharField(blank=True, max_length=128, null=True, verbose_name='Tomcat中文别名')),
                ('deploy_path', models.CharField(default='/local/server/', max_length=128, verbose_name='Tomcat部署路径')),
                ('version', models.CharField(blank=True, max_length=128, null=True, verbose_name='Tomcat版本')),
                ('ip4_inner', models.CharField(blank=True, max_length=32, null=True, verbose_name='内网IP_v4')),
                ('ip4_outer', models.CharField(blank=True, max_length=32, null=True, verbose_name='外网IP_v4')),
                ('http_port', models.SmallIntegerField(verbose_name='HTTP端口')),
                ('shutdown_port', models.SmallIntegerField(verbose_name='SHUTDOWN端口')),
                ('ajp_port', models.SmallIntegerField(verbose_name='AJP端口')),
                ('state', models.SmallIntegerField(verbose_name='运行状态')),
                ('config', models.TextField(blank=True, null=True, verbose_name='配置文件')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('remark', models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='备注')),
            ],
            options={
                'db_table': 'tomcat_server',
            },
        ),
        migrations.CreateModel(
            name='TomcatServerRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16)),
                ('record_type', models.SmallIntegerField(choices=[(1, '启动'), (2, '停止'), (3, '重启'), (4, '升级'), (5, '回滚')])),
                ('summary', models.CharField(max_length=256)),
                ('detail', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('tomcat_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cyeap_tomcat.TomcatServer')),
            ],
            options={
                'db_table': 'tomcat_server_record',
            },
        ),
        migrations.CreateModel(
            name='TomcatWebapp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='项目编号')),
                ('alias', models.CharField(blank=True, max_length=128, null=True, verbose_name='项目中文别名')),
                ('deploy_path', models.CharField(default='/local/webapp/', max_length=128, verbose_name='项目部署路径')),
                ('source_path', models.CharField(max_length=128, verbose_name='源路径')),
                ('current_version', models.CharField(blank=True, max_length=128, null=True, verbose_name='项目版本')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('remark', models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='备注')),
            ],
            options={
                'db_table': 'tomcat_webapp',
            },
        ),
        migrations.AddField(
            model_name='tomcatserver',
            name='webapp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cyeap_tomcat.TomcatWebapp', verbose_name='部署应用'),
        ),
    ]
