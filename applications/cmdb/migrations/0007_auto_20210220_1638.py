# Generated by Django 3.1.5 on 2021-02-20 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0006_auto_20210220_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='关系名称')),
            ],
        ),
        migrations.CreateModel(
            name='SchemaThroughRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='_parent', to='cmdb.cischema')),
                ('parent', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='_child', to='cmdb.cischema')),
                ('relation', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='ci_schema', to='cmdb.relation')),
            ],
            options={
                'verbose_name': '模型和关系穿梭表',
            },
        ),
        migrations.AddField(
            model_name='cischema',
            name='relation',
            field=models.ManyToManyField(related_name='relation_schema', through='cmdb.SchemaThroughRelation', to='cmdb.CISchema'),
        ),
    ]
