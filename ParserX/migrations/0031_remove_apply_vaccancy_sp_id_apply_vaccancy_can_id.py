# Generated by Django 5.1.4 on 2025-01-09 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0030_apply_vaccancy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apply_vaccancy',
            name='sp_id',
        ),
        migrations.AddField(
            model_name='apply_vaccancy',
            name='can_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ParserX.candidate'),
        ),
    ]
