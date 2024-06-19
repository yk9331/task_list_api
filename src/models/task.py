from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT

from src.db.base_class import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(String(256), nullable=False)
    status = Column(TINYINT, nullable=False, default=0)
