# Generated by Django 2.0.3 on 2019-12-26 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0013_remove_reaction_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(max_length=1000),
        ),
    ]