# Generated by Django 4.1.7 on 2023-06-19 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0015_tipo_alter_produto_categoria_alter_produto_tipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variacao',
            name='cores',
        ),
        migrations.DeleteModel(
            name='Cor',
        ),
    ]