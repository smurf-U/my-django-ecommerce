# Generated by Django 2.2 on 2020-05-02 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20200502_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='commitment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='confirm_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
