# Generated by Django 3.0.8 on 2022-04-04 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0007_auto_20220120_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='anulado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rendicion',
            name='anulada',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='registro',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
