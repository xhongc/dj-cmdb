# Generated by Django 3.1.7 on 2021-02-24 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0007_auto_20210220_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='relation',
            name='alias',
            field=models.CharField(default='', max_length=32, verbose_name='字段别名'),
        ),
    ]
