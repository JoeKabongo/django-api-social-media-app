# Generated by Django 2.0.3 on 2019-11-26 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0005_auto_20191125_0454'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reply',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
