# Generated by Django 5.0.4 on 2024-06-01 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("treasuries", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicaltreasury",
            name="miner",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="treasury",
            name="miner",
            field=models.BooleanField(default=False),
        ),
    ]
