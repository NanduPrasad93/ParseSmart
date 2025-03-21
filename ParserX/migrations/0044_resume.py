# Generated by Django 5.1.1 on 2025-01-31 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0043_alter_vaccancy_qualification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(upload_to='resumes/')),
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ParserX.candidate')),
            ],
        ),
    ]
