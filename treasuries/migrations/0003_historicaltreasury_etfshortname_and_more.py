# Generated by Django 5.0.4 on 2024-06-05 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("treasuries", "0002_historicaltreasury_miner_treasury_miner"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicaltreasury",
            name="etfshortname",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="treasury",
            name="etfshortname",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
