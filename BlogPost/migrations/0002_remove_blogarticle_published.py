# Generated by Django 2.0.3 on 2019-12-21 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogPost', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogarticle',
            name='published',
        ),
    ]
