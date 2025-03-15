# Generated by Django 5.1.1 on 2025-02-02 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParserX', '0055_category_question_userattempt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userattempt',
            name='category',
        ),
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
        migrations.RemoveField(
            model_name='userattempt',
            name='user',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='UserAttempt',
        ),
    ]
