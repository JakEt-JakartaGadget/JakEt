# Generated by Django 5.1.1 on 2024-10-24 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0005_phone_is_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]