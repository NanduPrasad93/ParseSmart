# Generated by Django 5.1.6 on 2025-03-07 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0080_remove_vaccancy_cad_delete_apply_vaccancy_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentralGovJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255, unique=True)),
                ('department', models.CharField(max_length=255)),
                ('field', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('required_qualifications', models.TextField()),
                ('age_limit_general', models.CharField(blank=True, max_length=50, null=True)),
                ('age_limit_obc', models.CharField(blank=True, max_length=50, null=True)),
                ('age_limit_sc_st', models.CharField(blank=True, max_length=50, null=True)),
                ('selection_process', models.TextField(blank=True, null=True)),
                ('salary_range', models.CharField(blank=True, max_length=100, null=True)),
                ('vacancies', models.IntegerField(blank=True, null=True)),
                ('exam_frequency', models.CharField(blank=True, max_length=100, null=True)),
                ('work_type', models.CharField(blank=True, choices=[('Permanent', 'Permanent'), ('Contract', 'Contract')], max_length=50, null=True)),
                ('application_mode', models.CharField(blank=True, choices=[('Online', 'Online'), ('Offline', 'Offline')], max_length=50, null=True)),
                ('requires_physical_fitness', models.BooleanField(default=False)),
                ('success_rate', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
