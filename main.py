import requests
from bs4 import BeautifulSoup
import json


# pip requests
# pip install bs4
# pip install lxml


def get_html(url, page=1):
    r = requests.get(url.format(page=page))
    return (r.text)


def get_counter_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_="pagination") \
        .find('ul', class_='pagination__list') \
        .find_all('a', class_='pagination__link')[-1]
    return int(pages.text)


def write_json(list_smart):
    with open("info.json", 'w') as outfile:
        json.dump(list_smart, outfile, indent=4, ensure_ascii=False)


def get_page_info(html, all_list_smart):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('ul', class_='catalog-grid') \
        .find_all('li', class_='catalog-grid__cell catalog-grid__cell_type_slim')

    for i in table:
        name = i.find('a', class_='goods-tile__heading')['title']\
            .replace('Мобильный телефон', "").strip()

        price = i.find('div', class_='goods-tile__prices')\
            .find('span', class_='goods-tile__price-value').text.strip()

        available = i.find('div', class_='goods-tile__availability').text

        info_smartfone = {'name': name, 'price': price, 'available': available}
        all_list_smart.append(info_smartfone)


def main():
    url = 'https://rozetka.com.ua/mobile-phones/c80003/page={page};producer=apple/'
    html = get_html(url)
    page_max = get_counter_pages(html)
    all_list_smart = []

    for i in range(1, page_max + 1):
        html = get_html(url, page=i)
        get_page_info(html, all_list_smart)

    write_json(all_list_smart)
    print("OK")


if __name__ == '__main__':
    main()
