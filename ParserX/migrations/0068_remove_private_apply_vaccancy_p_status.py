# Generated by Django 5.1.3 on 2025-02-11 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0067_rename_status_private_apply_vaccancy_p_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='private_apply_vaccancy',
            name='p_status',
        ),
    ]
