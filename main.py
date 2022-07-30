import time

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import json


def get_links():
    ua = UserAgent()
    url = 'https://hh.ru/search/vacancy?excluded_text=%D0%BF%D0%BE%D0%B4%D0%B4%D0%B5%D1%80%D0%B6%D0%BA%D0%B8%2C+NodeJS&schedule=remote&search_field=name&search_field=company_name&search_field=description&text=python&items_on_page=500&no_magic=true&L_save_area=true&page=0&hhtmFrom=vacancy_search_list'

    response = requests.get(url, headers={f'User-Agent': ua.random})

    soup = bs(response.content, 'lxml')
    page_count = int(soup.find('div', class_='pager').find_all('a')[-2].find('span').text)

    result = {}

    for page in range(page_count):
        url = f'https://hh.ru/search/vacancy?text=python&search_field=name&salary=&currency_code=RUR&experience=doesNotMatter&schedule=remote&order_by=relevance&search_period=0&items_on_page=50&no_magic=true&L_save_area=true&page={page}&hhtmFrom=vacancy_search_list'
        response = requests.get(url, headers={f'User-Agent': ua.random})
        soup = bs(response.content, 'lxml')
        vacancy_list = soup.find_all('div', class_='serp-item')

        for vacancy in vacancy_list:
            if 'hh.ru' not in vacancy.find('a', class_='bloko-link').attrs["href"]:
                continue
            vacancy_title = vacancy.find('a', class_='bloko-link').text
            vacancy_link = vacancy.find('a', class_='bloko-link').attrs["href"]
            vacancy_id = vacancy.find('a', class_='bloko-link').attrs["href"].split('/')[-1].split('?')[0]

            result[vacancy_id] = {
                    'Title': vacancy_title,
                    'Url': vacancy_link
                }
        print(f'Страница: {page} обработана.')
        time.sleep(4)
    with open('result.json', 'w') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)



def check_update_vacancy():
    new_vacancy = {}
    with open('result.json') as file:
        result = json.load(file)
    ua = UserAgent()
    url = 'https://hh.ru/search/vacancy?excluded_text=%D0%BF%D0%BE%D0%B4%D0%B4%D0%B5%D1%80%D0%B6%D0%BA%D0%B8%2C+NodeJS&schedule=remote&search_field=name&search_field=company_name&search_field=description&text=python&items_on_page=500&no_magic=true&L_save_area=true&page=1&hhtmFrom=vacancy_search_list'

    response = requests.get(url, headers={f'User-Agent': ua.random})

    soup = bs(response.content, 'lxml')
    vacancy_list = soup.find_all('div', class_='serp-item')

    for vacancy in vacancy_list:
        if 'hh.ru' not in vacancy.find('a', class_='bloko-link').attrs["href"]:
            continue
        vacancy_id = vacancy.find('a', class_='bloko-link').attrs["href"].split('/')[-1].split('?')[0]

        if vacancy_id in result:
            continue
        else:
            vacancy_title = vacancy.find('a', class_='bloko-link').text
            vacancy_link = vacancy.find('a', class_='bloko-link').attrs["href"]
            vacancy_id = vacancy.find('a', class_='bloko-link').attrs["href"].split('/')[-1].split('?')[0]
            print(vacancy_id)

            result[vacancy_id] = {
                'Title': vacancy_title,
                'Url': vacancy_link
            }
            new_vacancy[vacancy_id] = {
                'Title': vacancy_title,
                'Url': vacancy_link
            }
    if new_vacancy:
        print('Появились новые вакансии.')
    else:
        print('Нет новых вакансий.')
    with open('result.json', 'w') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    return new_vacancy


def main():
    # get_links()
    check_update_vacancy()

if __name__ == '__main__':
    main()
