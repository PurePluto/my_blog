# Generated by Django 2.0.4 on 2018-10-02 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readnum',
            name='read_num',
            field=models.IntegerField(default=0, verbose_name='统计数量'),
        ),
    ]
