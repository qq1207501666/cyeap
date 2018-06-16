# Generated by Django 2.0.3 on 2018-06-12 01:41

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('alias', models.CharField(blank=True, max_length=128, null=True)),
                ('version', models.CharField(blank=True, max_length=128, null=True)),
                ('deploy_path', models.CharField(max_length=128)),
                ('ip4_inner', models.CharField(blank=True, max_length=32, null=True)),
                ('ip4_outer', models.CharField(blank=True, max_length=32, null=True)),
                ('http_port', models.SmallIntegerField()),
                ('shutdown_port', models.SmallIntegerField()),
                ('ajp_port', models.SmallIntegerField()),
                ('is_run', models.BooleanField()),
                ('config', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('remark', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'db_table': 'TomcatServer',
            },
        ),
        migrations.CreateModel(
            name='TomcatWebapp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('alias', models.CharField(blank=True, max_length=128, null=True)),
                ('deploy_path', models.CharField(max_length=128)),
                ('source_path', models.CharField(max_length=128)),
                ('current_version', models.CharField(blank=True, max_length=128, null=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('remark', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'db_table': 'TomcatWebapp',
            },
        ),
        migrations.AddField(
            model_name='tomcatserver',
            name='webapp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cyeap_tomcat.TomcatWebapp'),
        ),
    ]
