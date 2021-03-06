# Generated by Django 3.2.9 on 2021-12-15 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('drops_collections', '0002_initial'),
        ('notifications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drops', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='from_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_user_notifications', to=settings.AUTH_USER_MODEL, verbose_name='From user'),
        ),
        migrations.AddField(
            model_name='notification',
            name='to_collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_collection_notifications', to='drops_collections.collection', verbose_name='To collection'),
        ),
        migrations.AddField(
            model_name='notification',
            name='to_drop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_drop_notifications', to='drops.drop', verbose_name='To drop'),
        ),
        migrations.AddField(
            model_name='notification',
            name='to_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_user_notifications', to=settings.AUTH_USER_MODEL, verbose_name='To user'),
        ),
    ]
