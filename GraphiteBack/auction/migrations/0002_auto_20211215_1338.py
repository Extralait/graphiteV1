# Generated by Django 3.2.9 on 2021-12-15 10:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_auction_bids'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionUserBid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Bid')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auction_user_bid', to='auction.auction', verbose_name='Auction')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auction_user_bid', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Auction user bid',
                'verbose_name_plural': 'Auction users bids',
            },
        ),
        migrations.DeleteModel(
            name='AuctionUserBid',
        ),
    ]
