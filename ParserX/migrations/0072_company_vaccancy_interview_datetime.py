# Generated by Django 5.1.3 on 2025-02-11 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0071_remove_company_vaccancy_interview_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_vaccancy',
            name='interview_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
