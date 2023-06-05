# Generated by Django 4.1.7 on 2023-06-05 10:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0011_contasreceber_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiado',
            name='data_p',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data do pagamento'),
        ),
        migrations.AlterField(
            model_name='fiado',
            name='data',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data da compra'),
        ),
    ]
