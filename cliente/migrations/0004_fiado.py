# Generated by Django 4.1.7 on 2023-04-26 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_alter_cliente_nome'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fiado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data do pagamento')),
                ('valor', models.FloatField(verbose_name='Valor da dívida')),
                ('pagamento', models.CharField(max_length=100)),
                ('cliente', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='cliente.cliente', verbose_name='Cliente')),
            ],
        ),
    ]
