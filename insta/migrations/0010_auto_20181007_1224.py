# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-07 12:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0009_likes_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='l_user', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
