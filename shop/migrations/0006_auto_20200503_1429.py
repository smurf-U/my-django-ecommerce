# Generated by Django 2.2 on 2020-05-03 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200503_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlines',
            name='unit_price',
            field=models.FloatField(null=True, verbose_name='Price'),
        ),
    ]
