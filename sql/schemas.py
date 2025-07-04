from pydantic import BaseModel
from qrcodegenerator import get_qrcode

class RssBase(BaseModel):
    rssname: str
    # pass
        
class TopicBase(BaseModel):
    topic: str
    # pass
    
class NewsBase(BaseModel):
    rssname: str
    title: str   
    description: str 
    
class Stdnotice(BaseModel):
    id: int
    title: str
    date: str
    type: str

    class Config:
        orm_mode = True


class Welfare(BaseModel):
    id: int
    type: str
    title: str
    target: str
    description: str

    class Config:
        orm_mode = True

class Rss(RssBase):
    link: str
    
    class Config:
        orm_mode = True
    
class Rss_topic(RssBase, TopicBase):
    # rss_id: int
    # topic_id: int
    link: str

    class Config:
        orm_mode = True
        
class Topic(TopicBase):
    id: int

    class Config:
        orm_mode = True
        
class News(NewsBase):
    link: str
    
    class Config:
        orm_mode = True
        
class TrendNewsQR(NewsBase):
    qrcode: str

    class Config:
        orm_mode = True

class TrendNewsOthers(NewsBase):
    qrcode: str
    #stdnotice: list
    #welfare: list
    
    class Config:
        orm_mode = True


def withQrcode(news: list, qrcode: str):
    a = NewsBase(rssname=news[0].rssname, title=news[0].title, description=news[0].description)
    data = TrendNewsQR(**a.dict(), qrcode = qrcode)
    return data

def withOthers(news: list, qrcode: str, stdnotice: list, welfare: list):
    a = NewsBase(rssname=news[0].rssname, title=news[0].title, description=news[0].description)
    data = TrendNewsOthers(**a.dict(), qrcode = qrcode, stdnotice = stdnotice, welfare = welfare)
    return data
