# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-27 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_question_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=20),
        ),
    ]
