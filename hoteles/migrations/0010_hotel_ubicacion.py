# Generated by Django 5.0.6 on 2024-07-06 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0009_reserva_fecha_salida'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='ubicacion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]