import sqlite3

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


BaseModel = declarative_base()


class Person(BaseModel):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    age = Column(Integer, nullable=True)
