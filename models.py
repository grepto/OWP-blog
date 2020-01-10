import random

from sqlalchemy import create_engine, Integer, Column, String, Text, Boolean, ForeignKey, Date, Table

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.sql import func

from faker import Faker

Base = declarative_base()
engine = create_engine('sqlite:///blog.sqlite')

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

fake = Faker()

tags_posts_table = Table(
    'tags_posts',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False)

    posts = relationship('Post', back_populates='author')


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(16), nullable=False)
    text = Column(Text, nullable=False)
    published = Column(Date, nullable=True)

    author = relationship(User, back_populates='posts')
    tags = relationship('Tag', secondary=tags_posts_table, back_populates='posts')

    def __repr__(self):
        return f'<Post #{self.id} - {self.title}>'


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)

    posts = relationship('Post', secondary=tags_posts_table, back_populates='tags')

    def __repr__(self):
        return f'<Tag #{self.id} - {self.name}>'


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
    """Creating database and load some demo content

    Run only if you need database with demo data"""

    crate_users_and_posts(session, 'Tuchka')
    crate_users_and_posts(session, 'Kesha')
    create_tags(session)
    set_tags(session)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()

    # uncomment row below in first launch
    # initialize()

    q = session.query(Post)\
        .join(User)\
        .join(tags_posts_table)\
        .join(Tag)\
        .filter(User.username == 'Kesha')\
        .having(func.count(Tag.id) == 2)\
        .group_by(Post.id)\

    print(q.all())
