# Generated by Django 2.0.3 on 2018-06-10 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0003_auto_20180610_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
