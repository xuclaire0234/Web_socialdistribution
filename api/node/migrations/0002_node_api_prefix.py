# Generated by Django 3.2.18 on 2023-03-26 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='api_prefix',
            field=models.CharField(default='api/', max_length=128),
        ),
    ]
