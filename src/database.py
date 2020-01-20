from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.models import Base

engine = create_engine('sqlite:///blog.sqlite')

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base.metadata.create_all(engine)
session = Session()
