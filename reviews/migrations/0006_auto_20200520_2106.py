# Generated by Django 2.2.5 on 2020-05-20 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20200520_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='accuracy',
            field=models.IntegerField(choices=[(0, 'I need some help!'), (1, "I'm really upset"), (2, "I've got a problem"), (3, 'Things are pretty good'), (4, 'Feeling Great!'), (5, 'Fantistic')], default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='check_in',
            field=models.IntegerField(choices=[(0, 'I need some help!'), (1, "I'm really upset"), (2, "I've got a problem"), (3, 'Things are pretty good'), (4, 'Feeling Great!'), (5, 'Fantistic')], default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='cleanliness',
            field=models.IntegerField(choices=[(0, 'I need some help!'), (1, "I'm really upset"), (2, "I've got a problem"), (3, 'Things are pretty good'), (4, 'Feeling Great!'), (5, 'Fantistic')], default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='communication',
            field=models.IntegerField(choices=[(0, 'I need some help!'), (1, "I'm really upset"), (2, "I've got a problem"), (3, 'Things are pretty good'), (4, 'Feeling Great!'), (5, 'Fantistic')], default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='location',
            field=models.IntegerField(choices=[(0, 'I need some help!'), (1, "I'm really upset"), (2, "I've got a problem"), (3, 'Things are pretty good'), (4, 'Feeling Great!'), (5, 'Fantistic')], default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='value',
            field=models.IntegerField(choices=[(0, 'I need some help!'), (1, "I'm really upset"), (2, "I've got a problem"), (3, 'Things are pretty good'), (4, 'Feeling Great!'), (5, 'Fantistic')], default=0),
        ),
    ]
