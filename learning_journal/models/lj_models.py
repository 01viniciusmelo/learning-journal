"""Model."""


from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
    Boolean,
)

from .meta import Base


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

    def to_json(self):
        """Convert to JSON."""
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "bio": self.bio,
        }
