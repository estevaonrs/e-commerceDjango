# Generated by Django 4.1.7 on 2023-06-26 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0014_remove_cliente_expiracao_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='codigo_temporario_expiracao',
        ),
        migrations.AddField(
            model_name='cliente',
            name='codigo_permanente',
            field=models.BooleanField(default=False, verbose_name='Código permanente'),
        ),
    ]
