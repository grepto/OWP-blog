from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

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

    def __repr__(self):
        return f'<User #{self.id} - {self.username}>'


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
