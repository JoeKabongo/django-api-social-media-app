# Generated by Django 2.0.3 on 2019-12-30 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogPost', '0005_blogarticle_blurb'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogarticle',
            old_name='titleImageLink',
            new_name='coverImage',
        ),
    ]
