# Generated by Django 2.0.3 on 2019-10-29 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0005_auto_20191029_0024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='user_receiver',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='user_sender',
        ),
        migrations.DeleteModel(
            name='Friend',
        ),
    ]
