# Generated by Django 4.1.7 on 2023-06-26 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0012_fiado_data_p_alter_fiado_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='expiracao',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
