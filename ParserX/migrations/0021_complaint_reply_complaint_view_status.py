# Generated by Django 5.1.4 on 2025-01-06 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0020_complaint_created_datetime_complaint_login_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='reply',
            field=models.CharField(default=0, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='complaint',
            name='view_status',
            field=models.IntegerField(default=0),
        ),
    ]
