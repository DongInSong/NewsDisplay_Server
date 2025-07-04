import logging
import sched
from sqlite3 import OperationalError
import threading
import time
from fastapi import FastAPI, Depends, Request, Response

from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionLocal, engine
# from api.apis import load_data, templates, data, live_stream
from api.news import load_data, pick_trendnews, pick_trendnews_keyword, getDF, getResult
from api.stdnotice import load_stdnotice
from api.welfare import load_welfare
from qrcodegenerator import get_qrcode

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
# app.mount("/static", StaticFiles(directory="../static"), name="static")
# templates = Jinja2Templates(directory="../templates")

logging.basicConfig(
  format = '[%(asctime)s] %(levelname)s: %(message)s',
  datefmt = '%I:%M:%S',
  level = logging.INFO
)

def get_news(sc):
    newsDB = SessionLocal()
    try:
        try:
            logging.info("Deleting news")
            crud.delete_trendnews(newsDB)
            crud.delete_news(newsDB)
            logging.info("Collecting news")
            load_data(newsDB)
            logging.info("News loaded")
        except OperationalError as e:
            logging.warning(e)
        try:
            logging.info("Selecting trendnews")
            for n in range(1, 9):
                logging.info(f'Category: {n}')
                df_kor, df_eng = getDF(newsDB, "category", n)
                pick_trendnews(newsDB, getResult(df_kor))
                pick_trendnews(newsDB, getResult(df_eng))
            logging.info("Trendnews loaded")
        except OperationalError as e:
            logging.warning(e)
    finally:
        newsDB.close()

def get_trendnews_keyword(sc, value):
    trendnewsDB = SessionLocal()
    global trendnews_keyword
    try:
        logging.info("Selecting trendnews with Keyword")
        df_kor, df_eng = getDF(trendnewsDB, "keyword", value)
        trendnews_keyword = pick_trendnews_keyword(getResult(df_kor))
        logging.info("Trendnews loaded")
        #stdnotice = crud.get_stdnotice(trendnewsDB)
        #welfare = crud.get_welfare(trendnewsDB)
        qrcode = get_qrcode(trendnews_keyword[0].link)
        #trendnews_keyword = schemas.withOthers(trendnews_keyword, qrcode, stdnotice, welfare)
        trendnews_keyword = schemas.withQrcode(trendnews_keyword, qrcode)
    except OperationalError as e:
            logging.warning(e)
    finally:
        trendnewsDB.close()

def get_stdnotice(sc):
    stdDB = SessionLocal()
    try:
        logging.info("Deleting stdnotice")
        crud.delete_stdnotice(stdDB)
        logging.info("Collecting stdnotice")
        insert_stdnotice(stdDB)
        logging.info("Stdnotice loaded")
    except OperationalError as e:
        logging.warning(e)
    finally:
        stdDB.close()
        
def get_welfare(sc):
    welDB = SessionLocal()
    try:
        logging.info("Deleting welfare")
        crud.delete_welfare(welDB)
        logging.info("Collecting welfare")
        load_welfare(welDB, "청년")
        logging.info("Welfare loaded")
    except OperationalError as e:
        logging.warning(e)
    finally:
        welDB.close()

s = sched.scheduler(time.time, time.sleep)
def collectNews():
    s.enter(5, 1, get_news, (s,))
    s.run()
    
def collectTrendnews_keyword(value):
    s.enter(1, 1, get_trendnews_keyword, (s, value))
    s.run()

def collectStdnotice():
    s.enter(5, 1, get_stdnotice, (s,))
    s.run()

def collectWelfare():
    s.enter(5, 1, get_welfare, (s, ))
    s.run()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
# @repeat_every(seconds = 40 * 60)# 5min
async def on_start():
    threading.Thread(target=collectNews).start()
    threading.Thread(target=collectStdnotice).start()
    threading.Thread(target=collectWelfare).start()
    print("a")

@app.on_event("shutdown")
def shutdown_event():
    SessionLocal().close
    
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/")
async def root():
    return 0


@app.get("/rss", response_model=list[schemas.Rss])
async def read_RSS(db: Session = Depends(get_db)):
    rss = crud.get_RSS(db)
    return rss

@app.get("/rss/topiclist", response_model=list[schemas.Topic])
async def read_TopicList(db: Session = Depends(get_db)):
    topicList = crud.get_topics(db)
    return topicList

@app.get("/rss/all", response_model=list[schemas.Rss])
async def read_all(db: Session = Depends(get_db)):
    rss_all = crud.get_RSS_All(db)
    return rss_all

@app.get("/rss/{topic}", response_model=list[schemas.Rss_topic])
async def read_RSS_topic(topic: str, db: Session = Depends(get_db)):
    rss_topic = crud.get_RSS_topic(db, topic = topic)
    return rss_topic

@app.get("/news", response_model=list[schemas.News])
async def read_news(db: Session = Depends(get_db)):
    news = crud.get_news_all(db)
    return news

@app.get("/news/category/{topicid}", response_model=list[schemas.News])
async def read_news_topic_byid(topicid: int, db: Session = Depends(get_db)):
    news = crud.get_news_topic_byid(db, topicid)
    return news

# @app.get("/news/{num}", response_model=schemas.TrendNewsQR)
# async def read_news(num: int, db: Session = Depends(get_db)):
#     news = crud.get_news(db, num)
#     qrcode = get_qrcode(news[0].link)
#     data = schemas.withQrcode(news, qrcode)
#     return data

@app.get("/news/{keyword}", response_model=list[schemas.News])
async def read_news_keyword(keyword: str, db: Session = Depends(get_db)):
    news = crud.get_news_keyword(db, keyword)
    print(type(news))
    return news


@app.get("/trendnewsKeyword/{keyword}", response_model=schemas.TrendNewsQR)
def read_trendnews_keyword(keyword: str):
    threading.Thread(target=collectTrendnews_keyword(keyword)).start()
    return trendnews_keyword

@app.get("/trendnews/{topic}", response_model=schemas.TrendNewsQR)
async def read_trendnews(topic: str, db: Session = Depends(get_db)):
    news = crud.get_trendnews(db, topic)
    #stdnotice = crud.get_stdnotice(db)
    #welfare = crud.get_welfare(db)
    qrcode = get_qrcode(news[0].link)
    #data = schemas.withOthers(news, qrcode, stdnotice, welfare)
    data = schemas.withQrcode(news, qrcode)
    return data


@app.delete("/news")
async def delete_news(db: Session = Depends(get_db)):
    crud.delete_news(db)

@app.post("/news")
async def insert_news(db: Session = Depends(get_db)):
    load_data(db)
    
@app.post("/trendnews")
async def insert_trendnews(db: Session = Depends(get_db)):
    pick_trendnews(db)
    
@app.delete("/trendnews")
async def delete_trendnews(db: Session = Depends(get_db)):
    crud.delete_trendnews(db)
    

@app.get("/stdnotice", response_model=list[schemas.Stdnotice])
async def read_stdnotice(db: Session = Depends(get_db)):
    stdnotice = crud.get_stdnotice(db)
    return stdnotice

@app.post("/stdnotice")
def insert_stdnotice(db: Session = Depends(get_db)):
    for n in range(1, 4):
        load_stdnotice(db, n)

@app.delete("/stdnotice")
async def delete_stdnotice(db: Session = Depends(get_db)):
    crud.delete_stdnotice(db)
    

@app.get("/welfare", response_model=list[schemas.Welfare])
async def read_welfare(db: Session = Depends(get_db)):
    welfare = crud.get_welfare(db)
    return welfare


@app.post("/welfare/{target}")
def insert_welfare(target: str, db: Session = Depends(get_db)):
    load_welfare(db, target)


@app.delete("/welfare")
async def delete_welfare(db: Session = Depends(get_db)):
    crud.delete_welfare(db)

# @app.get("/json", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("json.html", {"request": request, "data": data})

# @app.get("/main", response_class=HTMLResponse)
# async def read_main_news(request: Request, db: Session = Depends(get_db)):
#     news = crud.get_news(db, 1)
#     qrcode = get_qrcode(news[0].link)
#     return templates.TemplateResponse("display.html", {"request": request, "news": news, "qrcode": qrcode})


# @app.get("/main/{num}", response_class=HTMLResponse)
# async def read_main_news(num: str, request: Request, db: Session = Depends(get_db)):
#     news = crud.get_news(db, num)
#     qrcode = get_qrcode(news[0].link)
#     return templates.TemplateResponse("display.html", {"request": request, "news": news, "qrcode": qrcode})


# @app.get("/clock", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("clock.html", {"request": request})


# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})


# @app.get("/split", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("split.html", {"request": request})


# @app.get("/uptime", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("uptime.html", {"request": request, "data": live_stream})
