# Generated by Django 5.0.6 on 2024-07-06 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0011_hotel_desayuno_incluido_hotel_gimnasio_hotel_piscina_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='fecha_ingreso',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]