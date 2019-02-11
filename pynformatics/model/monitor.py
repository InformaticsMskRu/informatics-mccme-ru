from sqlalchemy import Integer, Column, String

from pynformatics.model.meta import Base


class MonitorLink(Base):

    __tablename__ = 'monitor_link'
    __table_args__ = (
        {'schema': 'pynformatics'}
    )

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, nullable=False)
    link = Column(String(20), nullable=False)
    internal_link = Column(String(4096), nullable=True)
