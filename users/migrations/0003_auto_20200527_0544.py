# Generated by Django 2.2.5 on 2020-05-26 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200524_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.CharField(blank=True, choices=[('krw', 'KRW'), ('usd', 'USD'), ('eur', 'EUR'), ('cny', 'CNY'), ('jpy', 'JPY')], default='krw', max_length=3),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('ko', 'Korean'), ('en', 'English'), ('es', 'Español'), ('zh', '汉语·中文'), ('jp', '日本語')], default='ko', max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='superhost',
            field=models.BooleanField(default=False),
        ),
    ]
