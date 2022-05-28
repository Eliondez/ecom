from faker import Faker
from random import randint, random
from django.utils import timezone
from datetime import timedelta


def create_fake_tasks():
    print('CREATING TASKS')
