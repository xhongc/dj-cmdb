# Generated by Django 3.1.5 on 2021-02-20 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_auto_20210220_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cifield',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='字段名称'),
        ),
    ]
