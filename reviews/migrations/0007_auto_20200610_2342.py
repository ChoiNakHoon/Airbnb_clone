# Generated by Django 2.2.5 on 2020-06-10 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20200520_2106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-created',)},
        ),
    ]