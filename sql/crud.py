from sqlalchemy.orm import Session

import sql.models as models


def get_RSS(db: Session):
    return db.query(models.RSS).all()


def get_topics(db: Session):
    return db.query(models.topics).all()

def get_RSS_Link(db: Session):
    return db.query(models.RSS_topic).all()

def get_RSS_All(db: Session):
    return db.query(models.RSS_topic)\
        .join(models.RSS)\
        .add_columns(models.RSS.rssname, models.RSS.id, models.RSS_topic.link)\
        .order_by(models.RSS.id.desc()).all()
    # join(조인 할 테이블).add_columns(조인 테이블에 추가 될 컬럼).order_by(기준.desc())


def get_RSS_topic(db: Session, topic: str):
    return db.query(models.RSS_topic)\
        .join(models.RSS, models.topics)\
        .add_columns(models.RSS.rssname, models.RSS.id, models.topics.topic, models.RSS_topic.link)\
        .filter(models.topics.topic == topic).all()
        
def get_news_all(db: Session):
    return db.query(models.news)\
        .join(models.RSS)\
        .add_columns(models.RSS.rssname, models.news.title, models.news.description, models.news.link)\
        .all()
        

def get_news_topic_byid(db: Session, topic: int):
    return db.query(models.news)\
        .join(models.RSS)\
        .add_columns(models.RSS.rssname, models.news.rss_id, models.news.topic_id, models.news.title, models.news.description, models.news.link, models.news.date)\
        .filter(models.news.topic_id == topic)\
        .all()
        
def get_news_keyword_title(db: Session, keyword: str):
    return db.query(models.news)\
        .join(models.RSS)\
        .add_columns(models.RSS.rssname, models.news.rss_id, models.news.topic_id, models.news.title, models.news.description, models.news.link, models.news.date)\
        .filter(models.news.title.like("%" + keyword + "%"))\
        .all()

def get_news_keyword_desc(db: Session, keyword: str):
    return db.query(models.news)\
        .join(models.RSS)\
        .add_columns(models.RSS.rssname, models.news.rss_id, models.news.topic_id, models.news.title, models.news.description, models.news.link, models.news.date)\
        .filter(models.news.description.like("%" + keyword + "%"))\
        .all()
        
def get_news(db: Session, num: int):
    return db.query(models.news)\
        .join(models.RSS)\
        .add_columns(models.RSS.rssname, models.news.title, models.news.description, models.news.link)\
        .filter(models.news.id == num)\
        .all()
    # return db.query(models.news).all()
    

def get_trendnews(db: Session, topic: str):
    return db.query(models.trendnews)\
        .join(models.RSS, models.topics)\
        .add_columns(models.RSS.rssname, models.topics.topic, models.trendnews.title, models.trendnews.description, models.trendnews.link)\
        .filter(models.topics.topic == topic)\
        .all()
        
def get_stdnotice(db: Session):
    return db.query(models.stdnotice).all()

def get_welfare(db: Session):
    return db.query(models.welfare).all()

def delete_news(db: Session):
    db.query(models.news).delete()
    db.execute('alter table news auto_increment = 0')
    db.commit()
    
def delete_trendnews(db: Session):
    db.query(models.trendnews).delete()
    db.execute('alter table trendnews auto_increment = 0')
    db.commit()
    
def delete_stdnotice(db: Session):
    db.query(models.stdnotice).delete()
    db.execute('alter table stdnotice auto_increment = 0')
    db.commit()

def delete_welfare(db: Session):
    db.query(models.welfare).delete()
    db.execute('alter table welfare auto_increment = 0')
    db.commit()
    
def insert_news(db: Session, news: models.news):
    db.add(news)
    db.commit()
    
def insert_trendnews(db: Session, news: models.trendnews):
    db.add(news)
    db.commit()
    
def insert_stdnotice(db: Session, stdnotice: models.stdnotice):
    db.add(stdnotice)
    db.commit()

def insert_welfare(db: Session, welfare: models.welfare):
    db.add(welfare)
    db.commit()