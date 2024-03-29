# Generated by Django 4.1.7 on 2023-06-01 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0009_alter_fiado_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiado',
            name='status',
            field=models.CharField(choices=[('D', 'Devendo'), ('P', 'Pago')], default='D', max_length=1),
        ),
        migrations.AlterField(
            model_name='fiado',
            name='pagamento',
            field=models.CharField(choices=[('C', 'Cartão'), ('D', 'Dinheiro')], default='C', max_length=1),
        ),
    ]
