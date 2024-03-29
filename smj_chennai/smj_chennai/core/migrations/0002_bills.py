# Generated by Django 4.0.6 on 2022-10-13 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bills",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("bill_number", models.IntegerField(unique=True)),
                ("bill_amount", models.FloatField()),
                ("payment_mode", models.CharField(max_length=10)),
                ("payment_received_at", models.DateField()),
                ("payment_received", models.DateField()),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("remarks", models.CharField(max_length=500)),
                (
                    "party",
                    models.ForeignKey(
                        db_column="party",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.party",
                    ),
                ),
            ],
            options={
                "db_table": "bills",
            },
        ),
    ]
