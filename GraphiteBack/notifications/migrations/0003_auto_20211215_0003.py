# Generated by Django 3.2.9 on 2021-12-14 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='body',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Body'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='details',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Details'),
        ),
    ]
