# Generated by Django 3.1.5 on 2021-02-18 04:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Notas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notaalumno',
            name='titulo',
            field=models.CharField(max_length=150),
            preserve_default=False,
        ),
    ]
