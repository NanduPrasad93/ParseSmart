# Generated by Django 5.1.1 on 2025-01-29 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0038_rename_notification_notification_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('link', models.URLField()),
                ('resource_type', models.CharField(max_length=50)),
                ('field', models.CharField(max_length=50)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
