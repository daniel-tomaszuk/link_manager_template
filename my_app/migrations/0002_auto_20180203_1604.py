# Generated by Django 2.0.2 on 2018-02-03 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='link_displays',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='link',
            name='link_hash',
            field=models.SlugField(max_length=128, unique=True),
        ),
    ]
