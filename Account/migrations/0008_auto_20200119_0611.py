# Generated by Django 2.0.3 on 2020-01-19 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0007_useraccount_iswritter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='isWritter',
            new_name='isWriter',
        ),
    ]
