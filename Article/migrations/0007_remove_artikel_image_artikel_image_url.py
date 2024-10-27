# Generated by Django 5.1 on 2024-10-27 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0006_alter_artikel_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artikel',
            name='image',
        ),
        migrations.AddField(
            model_name='artikel',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
