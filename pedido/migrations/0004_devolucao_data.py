# Generated by Django 4.1.7 on 2023-05-29 13:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0003_devolucao_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='devolucao',
            name='data',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data da devolução'),
        ),
    ]
