# Generated by Django 5.1.1 on 2024-10-25 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0007_phonerating'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]