# Generated by Django 2.0.3 on 2018-06-22 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyeap_tomcat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tomcatserver',
            name='remark',
            field=models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='tomcatwebapp',
            name='remark',
            field=models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='tomcatwebapp',
            name='source_path',
            field=models.CharField(max_length=128, verbose_name='源路径'),
        ),
    ]
