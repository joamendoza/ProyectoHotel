# Generated by Django 5.0.6 on 2024-07-07 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0012_reserva_fecha_ingreso'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='checkout',
            field=models.BooleanField(default=False),
        ),
    ]
