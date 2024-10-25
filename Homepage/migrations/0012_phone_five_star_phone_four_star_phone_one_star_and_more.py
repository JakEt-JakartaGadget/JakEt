# Generated by Django 5.1.1 on 2024-10-25 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0011_remove_phone_is_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='five_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='phone',
            name='four_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='phone',
            name='one_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='phone',
            name='three_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='phone',
            name='two_star',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='PhoneRating',
        ),
    ]
