# Generated by Django 5.0.1 on 2024-02-02 02:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0017_alter_exchange_coinfrom_alter_exchange_cointo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.URLField(default='', max_length=1000, verbose_name='Иконка')),
                ('name', models.CharField(default='', max_length=50, verbose_name='Название')),
                ('symbol', models.CharField(default='', max_length=10, verbose_name='Валюта')),
                ('price', models.DecimalField(decimal_places=3, default=0, max_digits=20, verbose_name='Цена к доллару')),
                ('reserve', models.DecimalField(decimal_places=2, default=1091094.2, max_digits=20, verbose_name='Резерв')),
                ('is_available', models.BooleanField(default=True, verbose_name='Включение/Выключение')),
            ],
            options={
                'verbose_name': 'Банк',
                'verbose_name_plural': 'Банки',
            },
        ),
        migrations.AlterModelOptions(
            name='depositpayment',
            options={'verbose_name': 'Адрес', 'verbose_name_plural': 'Адреса'},
        ),
        migrations.AlterModelOptions(
            name='depositsettings',
            options={'verbose_name': 'Лимит', 'verbose_name_plural': 'Лимиты'},
        ),
        migrations.AlterModelOptions(
            name='exchange',
            options={'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.AddField(
            model_name='depositsettings',
            name='crypto',
            field=models.CharField(choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('USDT', 'USDT'), ('LTC', 'LTC'), ('RUB', 'RUB')], max_length=20, null=True, verbose_name='Валюта'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='dep_wallet',
            field=models.CharField(max_length=500, null=True, verbose_name='Ваш адрес'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='fio',
            field=models.CharField(max_length=500, null=True, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='depositpayment',
            name='address',
            field=models.CharField(max_length=1000, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='depositpayment',
            name='crypto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crypto.crypto', verbose_name='Монета'),
        ),
        migrations.AlterField(
            model_name='depositpayment',
            name='network',
            field=models.CharField(blank=True, choices=[('', ''), ('TRC-20', 'TRC-20'), ('BEP-20', 'BEP-20'), ('ERC-20', 'ERC-20')], default='', help_text='Указывать только на монеты где нужно', max_length=100, null=True, verbose_name='Сеть'),
        ),
        migrations.AlterField(
            model_name='depositpayment',
            name='qrcode',
            field=models.ImageField(upload_to='', verbose_name='QR-код'),
        ),
        migrations.AlterField(
            model_name='depositsettings',
            name='title',
            field=models.CharField(default='Изменить', editable=False, max_length=100, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='coinFrom',
            field=models.CharField(max_length=100, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='coinTo',
            field=models.CharField(max_length=100, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='status',
            field=models.CharField(choices=[('W', 'В ожидании'), ('P', 'Оплачено'), ('NP', 'Ошибка')], default='W', max_length=30, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='sumFrom',
            field=models.CharField(max_length=100, null=True, verbose_name='Из'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='sumTo',
            field=models.CharField(max_length=100, null=True, verbose_name='В'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='wallet',
            field=models.CharField(max_length=500, null=True, verbose_name='Адрес'),
        ),
    ]