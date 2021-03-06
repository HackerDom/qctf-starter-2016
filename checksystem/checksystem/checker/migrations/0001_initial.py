# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-05 14:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('flag', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='submit',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checker.Task'),
        ),
    ]
