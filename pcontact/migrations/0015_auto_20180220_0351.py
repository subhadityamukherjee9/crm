# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-20 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcontact', '0014_auto_20180220_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyassociation',
            name='year',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
