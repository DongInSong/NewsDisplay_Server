import requests
import xmltodict
import requests
from sql import crud, models


class Welfare:
    def __init__(self, title, dept, target, description):
        self.title = title
        self.dept = dept
        self.target = target
        self.description = description


def load_welfare(db, arg1):
    url = "http://apis.data.go.kr/B554287/NationalWelfareInformations/NationalWelfarelist"
    params = {
        'serviceKey': 'a6/EcaYI3Q3If3xB3y7ocusVv02c26cqlWtZe8pWCNW7aME6i0bJUTMWZTk1VoZ1VXOxkYw/2Y5KuoPILNA/Dw==',
        'callTp': 'L',
        'pageNo': '1',
        'numOfRows': '50',
        'lifeArray': '004',
        'srchKeyCode': '001'
    }
    response = requests.get(url, params=params)
    parsed_xml = xmltodict.parse(response.content)
    items = parsed_xml['wantedList']['servList']

    selected = []

    for item in items:
        title = item['servNm']
        dept = item['jurMnofNm']
        target = item['lifeArray']
        description = item['servDgst']
        if arg1 in title:
            selected.append(Welfare(title, dept, target, description))

    i = 0
    while (len(selected) < 2 and i < len(items)):
        if (len(selected) < 1):
            selected.append(
                Welfare(items[0]['servNm'], items[0]['jurMnofNm'], items[0]['lifeArray'], items[0]['servDgst']))
            selected.append(
                Welfare(items[1]['servNm'], items[1]['jurMnofNm'], items[1]['lifeArray'], items[1]['servDgst']))
        elif (items[i]['servNm'] not in selected[0].title):
            selected.append(
                Welfare(items[i]['servNm'], items[i]['jurMnofNm'], items[i]['lifeArray'], items[i]['servDgst']))
        i += 1
    
    for n in selected:
        item = models.welfare(
            type = n.dept,
            title = n.title,
            target = n.target,
            description = n.description
        )
        crud.insert_welfare(db, item)

# selected = getWelfare()

# print(f'{selected[0].title} --{selected[0].target} --{selected[0].dept}')
# print(f'{selected[1].title} --{selected[1].target} --{selected[1].dept}')
