# Generated by Django 3.1.3 on 2021-10-29 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20211029_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetphoto',
            name='has_deleted',
            field=models.BooleanField(default=False),
        ),
    ]