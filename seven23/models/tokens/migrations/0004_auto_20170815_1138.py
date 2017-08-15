# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-15 11:38
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0003_auto_20170224_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstracttoken',
            name='token',
            field=models.TextField(default=uuid.uuid4, max_length=32, unique=True, verbose_name='Token'),
        ),
    ]
