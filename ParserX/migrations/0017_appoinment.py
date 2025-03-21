# Generated by Django 5.1.4 on 2025-01-03 11:05

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0016_expert_achievements_expert_designation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appoinment',
            fields=[
                ('a_id', models.AutoField(primary_key=True, serialize=False)),
                ('Date', models.DateField(null=True)),
                ('Time', models.TimeField(null=True)),
                ('current_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('status', models.IntegerField(default=0)),
                ('c_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ParserX.candidate')),
                ('e_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ParserX.expert')),
            ],
        ),
    ]
