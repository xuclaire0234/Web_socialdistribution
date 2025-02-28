# Generated by Django 3.2.18 on 2023-03-23 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('follower_node_id', models.URLField(db_index=True, max_length=128, verbose_name='author who is following the followee')),
                ('followed_at', models.DateTimeField(auto_now_add=True, verbose_name='Followed At')),
                ('followee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followee', to=settings.AUTH_USER_MODEL)),
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'unique_together': {('follower_node_id', 'followee')},
            },
        ),
    ]
