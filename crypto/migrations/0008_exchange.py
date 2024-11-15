# Generated by Django 5.0.1 on 2024-01-27 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0007_depositsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coinFrom', models.CharField(max_length=100)),
                ('coinTo', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=500)),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
