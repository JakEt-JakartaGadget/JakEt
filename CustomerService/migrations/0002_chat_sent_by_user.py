# Generated by Django 5.1.2 on 2024-10-26 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomerService', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='sent_by_user',
            field=models.BooleanField(default=True),
        ),
    ]