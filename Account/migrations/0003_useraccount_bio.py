# Generated by Django 2.0.3 on 2019-10-15 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_auto_20191015_0257'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='bio',
            field=models.CharField(default='', max_length=200),
        ),
    ]
