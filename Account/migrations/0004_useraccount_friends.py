# Generated by Django 2.0.3 on 2019-10-17 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_useraccount_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='friends',
            field=models.IntegerField(default=0),
        ),
    ]
