# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-06-06 11:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_company', '0006_auto_20190606_0530'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfoliocompany',
            old_name='protfolio_company_link',
            new_name='portfolio_company_link',
        ),
    ]
