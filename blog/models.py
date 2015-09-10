import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime,\
ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base, engine
from flask.ext.login import UserMixin



class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    superuser = Column(Boolean, default='False')
    posts = relationship("Post", backref="author")
    comments = relationship("Comment", backref="author")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    description = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    pats = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey('users.id'))
    comments = comments = relationship("Comment", backref="post")

    def as_dictionary(self):
        datetime = self.datetime.strftime("%d/%m/%y")
        post= {
            "title": self.title,            
            "id": self.id, 
            "datetime": datetime, 
            "content": self.content,            
            "description" : self.description            
          }
        return post

class Comment(Base):
    __tablename__= "comments"
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=datetime.datetime.now)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))



Base.metadata.create_all(engine)
