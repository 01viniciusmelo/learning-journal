"""Model."""


from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
    Boolean,
)

from .meta import Base

from passlib.apps import custom_app_context as pwd_context


class Jentry(Base):
    """Journal entry model."""

    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    author_username = Column(Unicode)
    content = Column(Unicode)
    contentr = Column(Unicode)
    created = Column(DateTime)
    modified = Column(DateTime)
    category = Column(Unicode)

    def __init__(self, **kwargs):
        """User constructor."""
        self.title = kwargs['title']
        self.author_username = kwargs['author_username']
        self.content = kwargs['content']
        self.contentr = ''
        self.created = kwargs['created']
        self.modified = kwargs['modified']
        self.category = kwargs['category']

    def to_json(self):
        """Convert to JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "author_username": self.author_username,
            "content": self.content,
            "contentr": self.contentr,
            "created": self.created,
            "modified": self.modified,
            "category": self.category,
        }

    def __str__(self):
        """For Python 2."""
        return str(self.title)


class User(Base):
    """User model."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode, unique=True)
    password = Column(Unicode)
    firstname = Column(Unicode)
    lastname = Column(Unicode)
    email = Column(Unicode, unique=True)
    author = Column(Boolean)
    admin = Column(Boolean)
    bio = Column(Unicode)

    def __init__(self, **kwargs):
        """User constructor."""
        self.username = kwargs['username']
        self.password = pwd_context.hash(kwargs['password'])
        self.firstname = kwargs['firstname']
        self.lastname = kwargs['lastname']
        self.email = kwargs['email']
        self.author = kwargs['author']
        self.admin = kwargs['admin']
        self.bio = kwargs['bio']

    def to_json(self):
        """Convert to JSON."""
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "bio": self.bio,
        }

    def __str__(self):
        """For Python 2."""
        return str(self.username)
