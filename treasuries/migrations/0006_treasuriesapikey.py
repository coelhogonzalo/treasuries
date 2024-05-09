# Generated by Django 5.0.4 on 2024-05-08 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasuries', '0005_alter_historicaltreasury_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreasuriesAPIKey',
            fields=[
                ('id', models.CharField(editable=False, max_length=150, primary_key=True, serialize=False, unique=True)),
                ('prefix', models.CharField(editable=False, max_length=8, unique=True)),
                ('hashed_key', models.CharField(editable=False, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('name', models.CharField(default=None, help_text='A free-form name for the API key. Need not be unique. 50 characters max.', max_length=50)),
                ('revoked', models.BooleanField(blank=True, default=False, help_text='If the API key is revoked, clients cannot use it anymore. (This cannot be undone.)')),
                ('expiry_date', models.DateTimeField(blank=True, help_text='Once API key expires, clients cannot use it anymore.', null=True, verbose_name='Expires')),
                ('hit_count', models.IntegerField(default=0, help_text='Number of times this API key has been used.')),
                ('data_used', models.FloatField(default=0, help_text='Amount of data used (in megabytes).')),
                ('last_used', models.DateField(default=None, help_text='Date when this API key was last used.', null=True)),
            ],
            options={
                'verbose_name': 'API key',
                'verbose_name_plural': 'API keys',
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
    ]