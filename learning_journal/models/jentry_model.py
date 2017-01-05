"""Model."""


from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
)

from .meta import Base


class Jentry(Base):
    """Journal entry constructor."""

    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    content = Column(Unicode)
    contentr = Column(Unicode)
    created = Column(DateTime)
    modified = Column(DateTime)
    category = Column(Unicode)
