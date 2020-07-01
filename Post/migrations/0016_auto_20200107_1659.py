# Generated by Django 2.0.3 on 2020-01-07 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BlogPost', '0006_auto_20191230_2212'),
        ('Post', '0015_auto_20200103_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='reaction',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article', to='BlogPost.BlogArticle'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='reply',
            name='content',
            field=models.CharField(max_length=1000),
        ),
    ]