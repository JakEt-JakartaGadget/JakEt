# Generated by Django 5.1.1 on 2024-10-25 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authenticate', '0001_initial'),
        ('Homepage', '0011_remove_phone_is_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='favorite_phones',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='Homepage.phone'),
        ),
    ]
