import os

from django.core.management.base import BaseCommand
import random
import string

from users.models import User
from config.settings import MEDIA_ROOT

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


def take_files_names(dir_path):
    files = []
    for subdir, dirs, files in os.walk(dir_path):
        for file in files:
            files.append(subdir + os.sep + file)
    return files


class Command(BaseCommand):
    help = 'Fill db'  # Описание команды

    def handle(self, *args, **kwargs):
        # Проходим по всем именам и создаём для каждого имени кота
        AVATARS = take_files_names(os.path.join(MEDIA_ROOT, "user/avatars/"))
        PICTURES_BIG = take_files_names(os.path.join(MEDIA_ROOT, "drop/picture_big/"))
        PICTURES_SMALL = take_files_names(os.path.join(MEDIA_ROOT, "drop/picture_small/"))

        for i in range(1000):
            user, create = User.objects.get_or_create(
                wallet_number=f'user {i}',
                owner_key=f'{i}',
                password={i}
            )
            if create:
                user.inn = str(random.randint(1000000000000000, 9999999999999999))
                user.balance = random.randint(0, 1000000)
                user.first_name = random.choice(FIRST_NAMES)
                user.last_name = random.choice(LAST_NAMES)
                user.avatar = random.choice(LAST_NAMES)

        print('All default cats updated. Have a nice day!')
