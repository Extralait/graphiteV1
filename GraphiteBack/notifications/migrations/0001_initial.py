# Generated by Django 3.2.9 on 2021-12-15 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('user_subscription', 'User subscription'), ('drop_subscription', 'Drop subscription'), ('collection_subscription', 'Collection subscription'), ('drop_like', 'Drop like'), ('collection_like', 'Collection like'), ('user_view', 'User view'), ('drop_view', 'Drop view'), ('collection_view', 'Collection view'), ('drop_put_up_for_sale', 'Drop put up for sale'), ('drop_buy', 'Drop buy'), ('offer', 'Offer'), ('confirm_offer', 'Confirm offer'), ('new_drop', 'New drop'), ('system', 'System')], max_length=50, verbose_name='Notification type')),
                ('header', models.CharField(blank=True, max_length=250, null=True, verbose_name='Header')),
                ('body', models.CharField(blank=True, max_length=500, null=True, verbose_name='Body')),
                ('details', models.CharField(blank=True, default='', max_length=500, verbose_name='Details')),
                ('is_viewed', models.BooleanField(default=False, verbose_name='Is viewed')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notification',
            },
        ),
    ]
