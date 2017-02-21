# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 12:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsnippet',
            name='language',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Language'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snip_author', to='account.UserProfile'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snip_lang', to='core.Language'),
        ),
    ]
