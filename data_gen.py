import csv
import random
import bcrypt

from typing import List

from faker import Faker
from uuid import uuid4

fake = Faker()

NUM_USERS = 100
NUM_RELATIONSHIPS = 1000
NUM_POSTS = 2000


def generate_user() -> List[str]:
    salt = bcrypt.gensalt()
    return [
        uuid4().hex,
        fake.name(),
        bcrypt.hashpw(fake.pystr(min_chars=5).encode(), salt),
    ]


def generate_relation(users: List[list]) -> List[str]:
    return [random.choice(users)[0], random.choice(users)[0], fake.date()]


def generate_posts(users: List[list]) -> List[str]:
    return [random.choice(users)[0], fake.paragraph(nb_sentences=1), fake.date()]


users = [generate_user() for _ in range(NUM_USERS)]
rels = [generate_relation(users) for _ in range(NUM_RELATIONSHIPS)]
posts = [generate_posts(users) for _ in range(NUM_POSTS)]

with open("data/users.csv", "w", newline="") as users_file:
    csv_writer = csv.writer(users_file)
    csv_writer.writerows(users)


with open("data/relationships.csv", "w", newline="") as rels_file:
    csv_writer = csv.writer(rels_file)
    csv_writer.writerows(rels)


with open("data/posts.csv", "w", newline="") as posts_file:
    csv_writer = csv.writer(posts_file)
    csv_writer.writerows(posts)
