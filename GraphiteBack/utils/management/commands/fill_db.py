import logging
import os
from bulk_update.helper import bulk_update

import datetime
from django.core.management.base import BaseCommand
import random
import string
import json

from django.utils.timezone import now
from lorem import get_paragraph

from auction.services.auction_operations import place_bid
from drops.models import Drop, Tag, Category
from drops.services.like import add_like as add_drop_like
from drops.services.subscription import add_subscription as add_drop_subscription
from drops.services.view import add_view as add_drop_view
from drops_collections.services.like import add_like as add_collection_like
from drops_collections.services.subscription import add_subscription as add_collection_subscription
from drops_collections.services.view import add_view as add_collection_view
from drops_collections.models import Collection
from offers.services.offer_operations import make_offer
from transactions.services.transaction_operations import buy_drop
from users.models import User
from config.settings import MEDIA_ROOT
from users.services.subscription import add_subscription as add_user_subscription
from users.services.view import add_view as add_user_view

FIRST_NAMES = [
    'Abraham', 'Addison', 'Adrian', 'Albert', 'Alec', 'Alfred', 'Alvin', 'Andrew', 'Andy', 'Archibald', 'Archie',
    'Arlo', 'Arthur', 'Arthur', 'Austen', 'Barnabe', 'Bartholomew', 'Bertram', 'Bramwell', 'Byam', 'Cardew', 'Chad',
    'Chance', 'Colin', 'Coloman', 'Curtis', 'Cuthbert', 'Daniel', 'Darryl', 'David', 'Dickon', 'Donald', 'Dougie',
    'Douglas', 'Earl', 'Ebenezer', 'Edgar', 'Edmund', 'Edward', 'Edwin', 'Elliot', 'Emil', 'Floyd', 'Franklin',
    'Frederick', 'Gabriel', 'Galton', 'Gareth', 'George', 'Gerard', 'Gilbert', 'Gorden', 'Gordon', 'Graham', 'Grant',
    'Henry', 'Hervey', 'Hudson', 'Hugh', 'Ian', 'Jack', 'Jaime', 'James', 'Jason', 'Jeffrey', 'Joey', 'John', 'Jolyon',
    'Jonas', 'Joseph', 'Joshua', 'Julian', 'Justin', 'Kurt', 'Lanny', 'Larry', 'Laurence', 'Lawton', 'Lester',
    'Malcolm', 'Marcus', 'Mark', 'Marshall', 'Martin', 'Marvin', 'Matt', 'Maximilian', 'Michael', 'Miles', 'Murray',
    'Myron', 'Nate', 'Nathan', 'Neil', 'Nicholas', 'Nicolas', 'Norman', 'Oliver', 'Oscar', 'Osric', 'Owen', 'Patrick',
    'Paul', 'Peleg', 'Philip', 'Phillipps', 'Raymond', 'Reginald', 'Rhys', 'Richard', 'Robert', 'Roderick', 'Rodger',
    'Roger', 'Ronald', 'Rowland', 'Rufus', 'Russell', 'Sebastian', 'Shahaf', 'Simon', 'Stephen', 'Swaine', 'Thomas',
    'Tobias', 'Travis', 'Victor', 'Vincent', 'Vincent', 'Vivian', 'Wayne', 'Wilfred', 'William', 'Winston', 'Zadoc'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson',
    'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark',
    'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'Hernandez', 'King', 'Wright', 'Lopez', 'Hill',
    'Scott', 'Green', 'Adams', 'Baker', 'Gonzalez', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner',
    'Phillips', 'Campbell', 'Parker', 'Evans', 'Edwards', 'Collins', 'Stewart', 'Sanchez', 'Morris', 'Rogers', 'Reed',
    'Cook', 'Morgan', 'Bell', 'Murphy', 'Bailey', 'Rivera', 'Cooper', 'Richardson', 'Cox', 'Howard', 'Ward', 'Torres',
    'Peterson', 'Gray', 'Ramirez', 'James', 'Watson', 'Brooks', 'Kelly', 'Sanders', 'Price', 'Bennett', 'Wood',
    'Barnes', 'Ross', 'Henderson', 'Coleman', 'Jenkins', 'Perry', 'Powell', 'Long', 'Patterson', 'Hughes', 'Flores',
    'Washington', 'Butler', 'Simmons', 'Foster', 'Gonzales', 'Bryant', 'Alexander', 'Russell', 'Griffin', 'Diaz',
    'Hayes'
]

SECIFICATIONS = ['height', 'width', 'size', 'saturation', 'depth', 'age', 'complexity']


def take_files_names(dir_path):
    files_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            print(dir_path+file)
            files_list.append((dir_path+file).split('media')[-1])
    return files_list


def random_string(length):
    s = string.ascii_lowercase + string.digits
    return ''.join(random.sample(s, length))


def create_specification():
    dict = {}
    random.shuffle(SECIFICATIONS)
    for key in SECIFICATIONS[:random.randint(1, len(SECIFICATIONS) - 1)]:
        dict[key] = random.randint(0, 1000)
    return json.dumps(dict, ensure_ascii=False, indent=4)


class Command(BaseCommand):
    help = 'Fill db'  # Описание команды

    def handle(self, *args, **kwargs):
        AVATARS = take_files_names(os.path.join(MEDIA_ROOT, "user/avatars/"))
        PICTURES_BIG = take_files_names(os.path.join(MEDIA_ROOT, "drop/picture_big/"))
        PICTURES_SMALL = take_files_names(os.path.join(MEDIA_ROOT, "drop/picture_small/"))

        tags = []
        categories = []
        users = []
        collections = []
        drops = []
        auctions = []
        for i in range(200):
            tag, create = Tag.objects.get_or_create(name=f'tag {i}')
            tags.append(tag)
        print('stop adding tags')
        print('start adding category')
        for i in range(50):
            category, create = Category.objects.get_or_create(name=f'category {i}')
            categories.append(category)
        print('stop adding tags')
        print('start adding users')
        for i in range(1000):
            user, create = User.objects.get_or_create(
                wallet_number=f'user {i}',
                defaults={
                    'owner_key': f'{i}',
                    'password': {i}
                },
            )
            user.inn = str(random.randint(1000000000000000, 9999999999999999))
            user.balance = random.randint(0, 1000000)
            user.first_name = random.choice(FIRST_NAMES)
            user.last_name = random.choice(LAST_NAMES)
            user.avatar = random.choice(AVATARS)
            user.profile_type = random.choice(['entity', 'individual'])
            user.profile_type = random.choice(['not_verified', 'moderation', 'verified'])
            user.email_notification = random.choice([True, False])
            user.description = get_paragraph()
            user.instagram = random_string(random.randint(5, 20))
            user.twitter = random_string(random.randint(5, 20))
            user.discord = random_string(random.randint(5, 20)) + '#' + str(random.randint(0, 9)) + str(
                random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
            user.tiktok = random_string(random.randint(5, 20))
            user.telegram = random_string(random.randint(5, 20))
            user.website = 'www' + random_string(random.randint(5, 20)) + '.com'
            users.append(user)
        bulk_update(users)
        print('stop adding users')

        for user in users:
            print('start adding collections and drops')
            for i in range(random.randint(3, 15)):
                collection, create = Collection.objects.get_or_create(
                    name=f'{user.wallet_number} collection {i}',
                    owner=user,
                    defaults={
                        'picture_big': random.choice(PICTURES_BIG),
                        'picture_small': random.choice(PICTURES_SMALL),
                    },
                )
                collections.append(collection)
                for j in range(random.randint(3, 15)):
                    random.shuffle(tags)
                    drop, create = Drop.objects.get_or_create(
                        name=f'{user.wallet_number} collection {i} drop {j}',
                        owner=user,
                        defaults={
                            'blockchain_type': random.choice(['wax', 'anchor']),
                            'descriptions': get_paragraph(),
                            'category': random.choice(categories),
                            'artist': user,
                            'sell_type': random.choice(['auction', 'sell']),
                            'sell_count': random.randint(1, 1000),
                            'all_count': random.randint(1001, 10000),
                            'init_cost': random.randint(1, 1000),
                            'min_rate': random.randint(1, 50),
                            'picture_big': random.choice(PICTURES_BIG),
                            'picture_small': random.choice(PICTURES_SMALL),
                            'to_sell': random.choice([False, True]),
                            'url_landing': 'https://www.google.com/',
                            'auction_deadline': str(now() + datetime.timedelta(seconds=random.randint(20000, 31104000))),
                            'royalty': abs(random.random()) * 100,
                            'specifications': create_specification(),
                            'from_collection': collection,
                            'level': random.randint(0, 100)
                        }
                    )
                    print(now() + datetime.timedelta(seconds=random.randint(20000, 31104000)))
                    drop.tags.set(tags[:random.randint(1, 15)])

                    drops.append(drop)

        for user in users:
            print('stop adding collections and drops')
            print('start adding user_subscriptions')
            for i in range(random.randint(10, 200)):
                subscription = random.choice(users)
                if subscription != user:
                    add_user_subscription(
                        subscription=subscription.pk,
                        subscriber=user.pk
                    )
            print('stop adding user_subscriptions')
            print('start adding user_views')
            for i in range(random.randint(10, 200)):
                overlooked = random.choice(users)
                if overlooked != user:
                    add_user_view(
                        overlooked=overlooked.pk,
                        looking=user.pk
                    )
            print('stop adding user_views')
            print('start adding drop_subscriptions')
            for i in range(random.randint(10, 200)):
                drop = random.choice(drops)
                if drop.owner != user:
                    add_drop_subscription(
                        drop=drop.pk,
                        user=user.pk
                    )
            print('stop adding drop_subscriptions')
            print('start adding drop_likes')
            for i in range(random.randint(10, 200)):
                drop = random.choice(drops)
                if drop.owner != user:
                    add_drop_like(
                        drop=drop.pk,
                        user=user.pk
                    )
            print('stop adding drop_likes')
            print('start adding drop_views')
            for i in range(random.randint(10, 200)):
                drop = random.choice(drops)
                if drop.owner != user:
                    add_drop_view(
                        drop=drop.pk,
                        user=user.pk
                    )
            print('stop adding drop_views')
            print('start adding collection_subscriptions')
            for i in range(random.randint(10, 200)):
                collection = random.choice(collections)
                if collection.owner != user:
                    add_collection_subscription(
                        collection=collection.pk,
                        user=user.pk
                    )
            print('stop adding collection_subscriptions')
            print('start adding collection_likes')
            for i in range(random.randint(10, 200)):
                collection = random.choice(collections)
                if collection.owner != user:
                    add_collection_like(
                        collection=collection.pk,
                        user=user.pk
                    )
            print('stop adding collection_likes')
            print('start adding collection_views')
            for i in range(random.randint(10, 200)):
                collection = random.choice(collections)
                if collection.owner != user:
                    add_collection_view(
                        collection=collection.pk,
                        user=user.pk
                    )
            print('stop adding collection_views')
            print('start adding buy_drop')
            for i in range(random.randint(1, 40)):
                try:
                    drop = random.choice(drops)
                    if drop.owner != user:
                        buy_drop(drop_pk=drop.pk,
                                 count=random.randint(1, 20),
                                 buyer=user)
                except:
                    continue
            print('stop adding buy_drop')
            print('start adding make_offer')
            for i in range(random.randint(1, 40)):
                try:
                    drop = random.choice(drops)
                    if drop.owner != user:
                        make_offer(drop_pk=drop.pk,
                                   count=random.randint(1, 20),
                                   unit_price=random.randint(10, 1000),
                                   buyer=user)
                except:
                    continue
            print('stop adding make_offer')
            print('start adding bids')
            random.shuffle(drops)
            for drop in drops[1:random.randint(5,30)]:
                for i in range(random.randint(1, 5)):
                    try:
                        auction = drop.auction.get(is_active=True)
                        if drop.owner != user:
                            place_bid(
                                auction_id=auction.pk,
                                user=user,
                                bid=random.randint(10, 100000)
                            )
                    except:
                        continue
            print('stop adding bids')
