# Generated by Django 4.1.7 on 2023-07-04 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0024_produto_cor_alter_produto_is_primary'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='modalidade',
            field=models.CharField(choices=[('A', 'Atacado'), ('V', 'Varejo')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='tipo',
            name='modalidade',
            field=models.CharField(choices=[('A', 'Atacado'), ('V', 'Varejo')], default='A', max_length=1),
        ),
    ]
