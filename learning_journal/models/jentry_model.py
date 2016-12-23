"""Model."""


from sqlalchemy import (
    Column,
    Integer,
    Unicode,
)

from .meta import Base


class Jentry(Base):
    """Journal entry constructor."""

    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    content = Column(Unicode)
    created = Column(Unicode)
    modified = Column(Unicode)
