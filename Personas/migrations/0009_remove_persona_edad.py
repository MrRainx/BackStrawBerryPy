# Generated by Django 3.1 on 2020-09-18 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Personas', '0008_auto_20200910_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='edad',
        ),
    ]