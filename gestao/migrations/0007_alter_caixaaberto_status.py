# Generated by Django 4.1.7 on 2023-05-31 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0006_caixaaberto_devolucao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caixaaberto',
            name='status',
            field=models.CharField(choices=[('A', 'Aberto'), ('F', 'Fechado')], default='A', max_length=1),
        ),
    ]
