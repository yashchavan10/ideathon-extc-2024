# Generated by Django 5.0.1 on 2024-03-29 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_disease_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disease_info',
            name='consultdoctor',
        ),
    ]
