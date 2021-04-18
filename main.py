import json

from bs4 import BeautifulSoup
import requests
import lxml

url = f'https://euro-rabota.com/'


def get_page(url):
    for i in range(1, 101):
        req = requests.get(f'{url}?page={i}')
        src = req.text

        with open(f'data/pages/{i}.html', 'w', encoding='utf-8') as f:
            f.write(src)


def read_page():
    res_dict = {}
    for i in range(1, 101):
        with open(f'data/pages/{i}.html', encoding='utf-8') as f:
            src = f.read()

        res = get_data(src)
        res_dict[i] = res

    with open(f'data/data_res.json', 'w', encoding='utf-8') as f:
        json.dump(res_dict, f, indent=4, ensure_ascii=False)


def get_data(src):
    soup = BeautifulSoup(src, 'lxml')
    items_dict = {}
    sections = soup.find_all(class_='vac-usual')
    for item in sections:
        title = item.find(class_='div-for-title').text.strip()
        country = item.find(class_='vac-place').text.strip()
        if item.find(class_='pay-ment'):
            payment = item.find(class_='pay-ment').text.strip()
        else:
            payment = 'None'
        if item.find(class_='profile-complete'):
            profile = item.find(class_='profile-complete').text.strip()
        else:
            profile = 'None'
        if item.find(class_='vac-rating-container'):
            date = item.find(class_='vac-rating-container').text.strip()
        else:
            date = 'None'

        items_dict[title] = {
            'title': title,
            'country': country,
            'payment': payment,
            'profile': profile,
            'date': date
        }
    return items_dict


if __name__ == '__main__':
    read_page()
    # get_page(url)
