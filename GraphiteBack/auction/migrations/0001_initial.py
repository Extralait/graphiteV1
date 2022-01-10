# Generated by Django 3.2.9 on 2021-12-15 12:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('init_cost', models.FloatField(verbose_name='Init cost')),
                ('current_cost', models.FloatField(verbose_name='Init cost')),
                ('min_rate', models.FloatField(verbose_name='Min rate')),
                ('sell_count', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Sell count')),
                ('auction_deadline', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Auction deadline')),
                ('royalty', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Royalty')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Auction',
                'verbose_name_plural': 'Auctions',
            },
        ),
        migrations.CreateModel(
            name='AuctionUserBid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Bid')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auction_user_bid', to='auction.auction', verbose_name='Auction')),
            ],
            options={
                'verbose_name': 'Auction user bid',
                'verbose_name_plural': 'Auction users bids',
            },
        ),
    ]