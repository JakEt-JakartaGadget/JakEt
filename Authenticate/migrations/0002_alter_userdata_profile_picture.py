# Generated by Django 5.1 on 2024-10-25 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authenticate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]