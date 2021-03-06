# Generated by Django 3.1.5 on 2021-01-20 04:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('Personas', '0005_personal_area_de_trabajo'),
        ('Matriculas', '0005_auto_20210114_2331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='periodolectivo',
            name='responsables',
        ),
        migrations.AddField(
            model_name='periodolectivo',
            name='coordinador',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='coordinador',
                to='Personas.personal'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='periodolectivo',
            name='sub_coordinador',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='sub_coordinador',
                to='Personas.personal'),
            preserve_default=False,
        ),
    ]
