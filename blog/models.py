from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    body = Column(String)
    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name,
            self.title,
            self.body,
            self.id,
        )