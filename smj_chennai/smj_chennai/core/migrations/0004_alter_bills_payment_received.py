# Generated by Django 4.0.6 on 2022-10-13 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_bills_payment_received_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='payment_received',
            field=models.FloatField(),
        ),
    ]