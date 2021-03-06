# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-06-02 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='company_team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('team_image', models.ImageField(blank=True, null=True, upload_to='team')),
                ('team_description', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('team_position', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('team_linkedin_url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
