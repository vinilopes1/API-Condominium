# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 01:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comum', '0003_condominio_sindico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominio',
            name='sindico',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='condominio', to='comum.Perfil'),
        ),
    ]