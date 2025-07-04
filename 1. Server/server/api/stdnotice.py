
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from sql import crud, models

def webCrawling(value):
    html_text = requests.get('https://www.kumoh.ac.kr/ko/sub06_01_01_0' + value + '.do')
    soup = BeautifulSoup(html_text.content, "html.parser")
    titlesFound = soup.find_all("span", {"class": "title-wrapper"})
    datesFound = soup.find_all("span", {"class": "mobile-info"})

    data_importants = {
        "title": [],
        "date": []
    }
    data_normal = {
        "title": [],
        "date": []
    }

    for title, date in zip(titlesFound, datesFound):
        if (len(title.contents) > 1):
            data_importants['title'].append(
                ' '.join(title.contents[2].split()))
            data_importants['date'].append(' '.join(date.contents[5]))
        else:
            data_normal['title'].append(' '.join(title.contents[0].split()))
            data_normal['date'].append(' '.join(date.contents[5]))

    return data_importants, data_normal


def selectNotice(data_importants, data_normal):
    selected = {
        "title": [],
        "date": []
    }
    # 주요 공지들 중에서 오늘 올라온 공지 있으면 고것부터 샥샥
    for title, date in zip(data_importants['title'], data_importants['date']):
        if (date == datetime.today().strftime('%Y-%m-%d')):
            selected['title'].append(title)
            selected['date'].append(date)

    # 일반 뉴스 중에서 오늘 올라온 공지 샥샥 추가
    for title, date in zip(data_normal['title'], data_normal['date']):
        if (date == datetime.today().strftime('%Y-%m-%d')):
            selected['title'].append(title)
            selected['date'].append(date)

    # 오늘 올라온 공지가 2개 미만이면 일반 공지에서 샥샥 채워넣기 (2개 될 때까지)
    i = 0
    while (len(selected['title']) < 2 and i < len(data_normal)):
        if (data_normal['date'][i] != datetime.today().strftime('%Y-%m-%d')):
            selected['title'].append(data_normal['title'][i])
            selected['date'].append(data_normal['date'][i])
        i = i + 1

    return selected


# 사용 예제

def load_stdnotice(db, category):
    if category == 1:
        type = "학사"
    elif category == 2:
        type = "행사"
    elif category == 3:
        type = "일반"
    
    data_importants, data_normal = webCrawling(str(category))
    selected = selectNotice(data_importants, data_normal)

    # title, date 둘 다 필요할 경우
    for title, date in zip(selected['title'], selected['date']):
        item = models.stdnotice(
            type = type,
            title = title,
            date = date
        )
        crud.insert_stdnotice(db, item)
        # print(item.type)
# crud.delete_stdnotice(db)
# title만 필요한 경우
# for title in selected['title']:
    # print(title)
