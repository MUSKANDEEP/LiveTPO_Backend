# Generated by Django 5.1.7 on 2025-04-16 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.RemoveField(
            model_name='interview',
            name='student',
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.DeleteModel(
            name='Interview',
        ),
    ]
