# Generated by Django 2.0.3 on 2019-11-28 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0012_reaction_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reaction',
            name='time',
        ),
    ]
