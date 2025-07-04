import time
from sql.database import SessionLocal, engine
from sql import crud, models, schemas
import requests
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import pandas as pd

import sys
sys.path.append('./server')


def load_data(db):
    start_time = time.time()
    rss = crud.get_RSS_Link(db)
    
    for n in rss:
        if (n.link != "-"):
            d = requests.get(n.link)
            soup = BeautifulSoup(d.content, 'xml')
            items = soup.find_all('item')
            for news in items:
                news.extract()
                try:
                    dirtyDes = news.description.text
                    description = BeautifulSoup(dirtyDes, "lxml").text
                    dirtyTitle = news.title.text
                    title = BeautifulSoup(dirtyTitle, "lxml").text
                    item = models.news(
                        rss_id=n.rss_id,
                        topic_id=n.topic_id,
                        title=title,
                        description=description,
                        link=news.link.text,
                        date=news.pubDate.text
                    )

                    crud.insert_news(db, item)

                except AttributeError: 
                    print("no description")

    print("--- %s seconds ---" % (time.time() - start_time))


# def pick_trendnews(db):
#     total_time = time.time()
#     for n in range(1, 9):
#         start_time = time.time()
#         news = crud.get_news_topic_byid(db, n)
#         df = pd.DataFrame(
#             columns=['title', 'description', 'link', 'date'])
#         for item in news:
#             row = {'title': item.title, 'description': item.description,
#                    'link': item.link, 'date': item.date}
#             df.loc[len(df)] = row
#         df = df[df['description'].notna()]
#         df = df[df['description'] != '']
#         df.reset_index(drop=True, inplace=True)
#         # print(df['title'], n)
#         count = 0
#         count_list = []
#         new_df = df
#         for index, row in df.iterrows():
#             test = df.iloc[index]['title']
#             test_desc = df.iloc[index]['description']
#             for indexAfter in range(1, len(new_df)):
#                 print(test, new_df.iloc[indexAfter]['title'])
#                 if SequenceMatcher(lambda z: z == " ", test_desc, new_df.iloc[indexAfter]['description']).ratio() > 0.13:
#                     count = count + 1  # count increases
#             count_list.append(count)
#             count = 0
#             new_df = new_df.iloc[1:]
#         df['count'] = count_list

#         result = df.loc[df['count'] == df['count'].max()]

#         for i in range(0, len(result)):
#             item = models.trendnews(
#                 rss_id=item.rss_id,
#                 topic_id=n,
#                 title=result.iloc[i]['title'],
#                 description=result.iloc[i]['description'],
#                 link=result.iloc[i]['link'],
#                 date=result.iloc[i]['date'],
#                 count=int(result.iloc[i]['count'])
#             )
#             print(n, "번 카테고리")
#             print(item.title)
#             print(item.count)
#             crud.insert_trendnews(db, item)
#         print("--- %s seconds ---" % (time.time() - start_time))

#     # db.close
#     print("--- %s seconds ---" % (time.time() - total_time))

def getDF(db, type, value):
    if (type == "category"): news = crud.get_news_topic_byid(db, value)
    else: 
        news = crud.get_news_keyword_title(db, value)
        print(" No title")
        if not news:
            news = crud.get_news_keyword_desc(db, value)
            if not news:
                print("No data")
                return 0
    
    df_kor = pd.DataFrame(
        columns=['rssname', 'rss_id', 'topic_id', 'title', 'description', 'link', 'date'])
    df_eng = pd.DataFrame(
        columns=['rssname', 'rss_id', 'topic_id', 'title', 'description', 'link', 'date'])

    for item in news:
        row = {'rssname': item.rssname, 'rss_id': item.rss_id, 'topic_id': item.topic_id, 'title': item.title, 'description': item.description,
               'link': item.link, 'date': item.date}
        if item.rss_id < 11:
            df_kor.loc[len(df_kor)] = row
        else:
            df_eng.loc[len(df_eng)] = row

    df_kor = dfCheck(df_kor)
    df_eng = dfCheck(df_eng)

    return df_kor, df_eng


def dfCheck(df):
    df = df[df['description'].notna()]
    df = df[df['description'] != '']
    df.reset_index(drop=True, inplace=True)
    return df


def getResult(df):
    count_list = []
    new_df = df
    for index, row in df.iterrows():
        # for index in range(0, 1):
        count = 0
        test = df.iloc[index]['title']
        test_desc = df.iloc[index]['description']
        for indexAfter in range(0, len(new_df)):
            # print(index, test, indexAfter, new_df.iloc[indexAfter]['title'])
            if SequenceMatcher(lambda z: z == " ", test_desc, new_df.iloc[indexAfter]['description']).ratio() > 0.13:
                count = count + 1  # count increases

        count_list.append(count)
        # new_df = new_df.iloc[1:]
    df['count'] = count_list
    result = df.loc[df['count'] == df['count'].max()]

    return result

def pick_trendnews_keyword(df_result):
    list = []
    for i in range(0, len(df_result)):
        item = models.trendnews(
            rssname=df_result.iloc[i]['rssname'],
            rss_id=df_result.iloc[i]['rss_id'],
            topic_id=df_result.iloc[i]['topic_id'],
            title=df_result.iloc[i]['title'],
            description=df_result.iloc[i]['description'],
            link=df_result.iloc[i]['link'],
            date=df_result.iloc[i]['date'],
            count=int(df_result.iloc[i]['count'])
        )
        print(item.topic_id, "번 카테고리")
        print(item.title)
        print(item.description)
        print(item.count)
        list.append(item)
    return list
        
def pick_trendnews(db, df_result):
    # print(result)
    for i in range(0, len(df_result)):
        item = models.trendnews(
            rssname=df_result.iloc[i]['rssname'],
            rss_id=df_result.iloc[i]['rss_id'],
            topic_id=df_result.iloc[i]['topic_id'],
            title=df_result.iloc[i]['title'],
            description=df_result.iloc[i]['description'],
            link=df_result.iloc[i]['link'],
            date=df_result.iloc[i]['date'],
            count=int(df_result.iloc[i]['count'])
        )
        print(item.topic_id, "번 카테고리")
        print(item.title)
        print(item.description)
        print(item.count)
        crud.insert_trendnews(db, item)

    # db.close


# start_time = time.time()
# # pick_trendnews(db, 1);
# # getResult(db, 1)
# # print(getDF(db, 1))

# print("--- %s seconds ---" % (time.time() - start_time))
