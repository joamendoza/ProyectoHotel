# Generated by Django 5.0.6 on 2024-07-06 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0010_usuario_lista_cupones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='comentarios_valoraciones',
        ),
    ]
