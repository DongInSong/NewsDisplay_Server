import datetime
import time
from xmlrpc.client import DateTime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sql.database import Base


def same_as(col): return lambda ctx: ctx.current_parameters.get(col)

class RSS(Base):
    __tablename__ = "rss"
    
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    rssname = Column(String)
    link = Column(String)
    
class topics(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    topic = Column(String)
    
class RSS_topic(Base):
    __tablename__ = "rss_topic"
    
    rss_id = Column(Integer, ForeignKey("rss.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), primary_key=True)
    link = Column(String)
    
    rss = relationship("RSS", backref = "rss_topic")
    topics = relationship("topics", backref = "rss_topic")

class news(Base):
    __tablename__ = "news"
    
    rss_id = Column(Integer, ForeignKey("rss.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), primary_key=True)
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    title = Column(String)
    description = Column(String, default=same_as('title'))
    link = Column(String)
    date = Column(String, default=datetime.datetime.now)
    # >>> method1 = datetime.strptime(pubdate, '%a, %d %b %Y %H:%M:%S %z')


class trendnews(Base):
    __tablename__ = "trendnews"

    rssname = Column(String)
    rss_id = Column(Integer, ForeignKey("rss.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), primary_key=True)
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    title = Column(String)
    description = Column(String, default=same_as('title'))
    link = Column(String)
    date = Column(String, default=datetime.datetime.now)
    count = Column(Integer)

class stdnotice(Base):
    __tablename__ = "stdnotice"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    type = Column(String)
    title = Column(String)
    date = Column(String, default=datetime.datetime.now)


class welfare(Base):
    __tablename__ = "welfare"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    type = Column(String)
    title = Column(String)
    target = Column(String)
    description = Column(String)