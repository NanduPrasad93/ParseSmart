# Generated by Django 5.1.4 on 2025-01-06 10:16

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0021_complaint_reply_complaint_view_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip_text', models.TextField()),
                ('created_datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tips', to='ParserX.category')),
            ],
        ),
    ]
