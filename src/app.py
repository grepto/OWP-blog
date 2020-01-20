from sqlalchemy.sql import func

from database import session
from filling_db import initialize
from src.models import Post, Tag, User, tags_posts_table

if __name__ == '__main__':
    initialize()

    q = session.query(Post)\
        .join(User)\
        .join(tags_posts_table)\
        .join(Tag)\
        .filter(User.username == 'Kesha')\
        .having(func.count(Tag.id) == 2)\
        .group_by(Post.id)\

    print(q.all())
