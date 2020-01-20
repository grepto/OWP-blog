import random

from faker import Faker

from database import session
from src.models import Post, Tag, User

fake = Faker()


def crate_users_and_posts(session, user_name):
    user = User(username=user_name)
    session.add(user)
    session.flush()

    for _ in range(3):
        post = Post(author_id=user.id, title=fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                    text=fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None))
        session.add(post)

    session.commit()


def create_tags(session):
    for _ in range(6):
        tag = Tag(name=fake.word(ext_word_list=None))
        session.add(tag)
    session.commit()


def set_tags(session):
    tags = session.query(Tag).all()
    posts = session.query(Post).all()

    for post in posts:
        random_tags = random.sample(tags, random.randint(1, 3))
        post.tags.extend(random_tags)

    session.commit()


def initialize():
    """Creating database and load some demo content"""

    if not session.query(Post).first():

        crate_users_and_posts(session, 'Tuchka')
        crate_users_and_posts(session, 'Kesha')
        create_tags(session)
        set_tags(session)
