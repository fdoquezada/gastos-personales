# Generated by Django 5.2 on 2025-05-07 03:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaccion',
            options={'ordering': ['-fecha_creacion']},
        ),
        migrations.AddField(
            model_name='transaccion',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
