# Generated by Django 5.1.4 on 2025-01-03 11:07

import ParserX.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0017_appoinment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appoinment',
            name='current_date',
            field=models.DateField(default=ParserX.models.Appoinment.get_current_date, null=True),
        ),
    ]
