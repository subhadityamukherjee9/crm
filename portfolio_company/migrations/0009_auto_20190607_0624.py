# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-06-07 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_company', '0008_portfoliocompany_short_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfoliocompany',
            name='portfolio_image_url',
        ),
        migrations.AddField(
            model_name='portfoliocompany',
            name='portfolio_background_image',
            field=models.ImageField(blank=True, null=True, upload_to='background'),
        ),
    ]
