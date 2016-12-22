"""Model."""


from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
)

from .meta import Base


class Entry(Base):
    """Journal entry constructor."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(Unicode)
    last_modified = Column(Unicode)


Index('my_index', Entry.title, unique=True, mysql_length=255)
