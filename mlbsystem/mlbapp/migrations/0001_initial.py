# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-28 10:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='backboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('backtime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='board',
            fields=[
                ('boardid', models.AutoField(primary_key=True, serialize=False)),
                ('boardcode', models.CharField(max_length=20)),
                ('sn', models.CharField(max_length=20)),
                ('config', models.CharField(max_length=50)),
                ('source', models.CharField(max_length=20)),
                ('teststatus', models.CharField(max_length=30)),
                ('storetime', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='delboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deltime', models.DateTimeField()),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlbapp.board')),
            ],
        ),
        migrations.CreateModel(
            name='loanboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loantime', models.DateTimeField()),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlbapp.board')),
            ],
        ),
        migrations.CreateModel(
            name='pro_cfg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_cfg', models.CharField(max_length=20)),
                ('totalnums', models.IntegerField()),
                ('loannums', models.IntegerField()),
                ('remainnums', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('usernum', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='loanboard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlbapp.user'),
        ),
        migrations.AddField(
            model_name='board',
            name='pro_cfg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlbapp.pro_cfg'),
        ),
        migrations.AddField(
            model_name='backboard',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlbapp.board'),
        ),
        migrations.AddField(
            model_name='backboard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlbapp.user'),
        ),
    ]
