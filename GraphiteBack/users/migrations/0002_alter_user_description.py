# Generated by Django 3.2.9 on 2021-12-14 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Description'),
        ),
    ]