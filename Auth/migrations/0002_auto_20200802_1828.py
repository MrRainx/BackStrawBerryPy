# Generated by Django 3.0.8 on 2020-08-02 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='permisos',
            field=models.ManyToManyField(to='Auth.Permiso'),
        ),
    ]
