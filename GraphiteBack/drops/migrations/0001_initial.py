# Generated by Django 3.2.9 on 2021-12-15 12:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=256, primary_key=True, serialize=False, unique=True, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Drop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blockchain_type', models.CharField(blank=True, choices=[('wax', 'WAX'), ('anchor', 'Anchor')], max_length=20, null=True, verbose_name='Blockchain type')),
                ('blockchain_address', models.CharField(blank=True, max_length=256, null=True, verbose_name='Blockchain address')),
                ('blockchain_identifier', models.CharField(blank=True, max_length=256, null=True, verbose_name='Blockchain identifier')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('descriptions', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('sell_type', models.CharField(blank=True, choices=[('auction', 'Auction'), ('sell', 'Sell')], max_length=20, null=True, verbose_name='Sell type')),
                ('sell_count', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Sell count')),
                ('in_stock', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='In Stock')),
                ('all_count', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='All count')),
                ('init_cost', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Init cost')),
                ('min_rate', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Min rate')),
                ('picture_big', models.ImageField(blank=True, null=True, upload_to='drop/picture_big', verbose_name='Big picture')),
                ('picture_small', models.ImageField(blank=True, null=True, upload_to='drop/picture_small', verbose_name='Small picture')),
                ('to_sell', models.BooleanField(blank=True, default=False, verbose_name='To sell')),
                ('url_landing', models.CharField(blank=True, max_length=256, null=True, verbose_name='Landing URL')),
                ('auction_deadline', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Auction deadline')),
                ('royalty', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Royalty')),
                ('specifications', models.JSONField(blank=True, null=True, verbose_name='Specifications')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('level', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Level')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Drop',
                'verbose_name_plural': 'Drops',
            },
        ),
        migrations.CreateModel(
            name='DropLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Drop like',
                'verbose_name_plural': 'Drop likes',
            },
        ),
        migrations.CreateModel(
            name='DropSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Drop subscription',
                'verbose_name_plural': 'Drops subscriptions',
            },
        ),
        migrations.CreateModel(
            name='DropView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Drop view',
                'verbose_name_plural': 'Drops views',
            },
        ),
        migrations.CreateModel(
            name='SpecialCollectionDrop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Level')),
            ],
            options={
                'verbose_name': 'Special collection drop',
                'verbose_name_plural': 'Special collections drops',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=256, primary_key=True, serialize=False, unique=True, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
    ]
