# Generated by Django 4.1.7 on 2023-05-29 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0004_devolucao_data'),
        ('gestao', '0005_caixaaberto_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='caixaaberto',
            name='devolucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedido.devolucao'),
        ),
    ]
