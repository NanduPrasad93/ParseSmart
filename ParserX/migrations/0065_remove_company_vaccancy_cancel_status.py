# Generated by Django 5.1.1 on 2025-02-09 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0064_company_vaccancy_cancel_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company_vaccancy',
            name='cancel_status',
        ),
    ]
