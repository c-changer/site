# Generated by Django 5.0.1 on 2024-01-27 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0010_exchange_sumfrom_exchange_sumto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
