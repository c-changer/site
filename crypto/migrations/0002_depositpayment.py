# Generated by Django 5.0.1 on 2024-01-25 04:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.CharField(blank=True, choices=[('', ''), ('TRC-20', 'TRC-20'), ('BEP-20', 'BEP-20'), ('ERC-20', 'ERC-20')], default='', help_text='Указывать только на монеты где нужно', max_length=100, null=True, verbose_name='Адрес для депозита')),
                ('qrcode', models.ImageField(upload_to='deposit_qrcodes/', verbose_name='QR-код для депозита')),
                ('address', models.CharField(max_length=1000, verbose_name='Адрес для депозита')),
                ('crypto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crypto.crypto', verbose_name='Монета для депозита')),
            ],
            options={
                'verbose_name': 'Информация для депозитов',
                'verbose_name_plural': 'Информация для депозитов',
            },
        ),
    ]
