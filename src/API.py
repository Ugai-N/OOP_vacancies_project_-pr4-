import os
from abc import ABC, abstractmethod
import datetime

import requests

from src.vacancy import Vacancy

SJ_API_KEY: str = os.getenv('SJ_API_KEY')


class AbstractAPI(ABC):
    '''абстрактный класс для работы с API сайтов с вакансиями.
    Наследники класса для каждой платформы подключаются к API и получают вакансии'''

    @abstractmethod
    def check_connection(self) -> int:
        '''функция для проверки статус-кода при работе с API'''
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str) -> list:
        '''обращается к API и выгружает список вакансии согласно запросу search_query'''
        pass

    @abstractmethod
    def initialize_vacancy(self, search_query: str) -> None:
        '''для каждой вакансии, найденной по запросу search_query, инициализирует экземпляр Vacancy'''
        pass


class HeadHunterAPI(AbstractAPI):
    '''Максимальное количество сущностей, выдаваемых API равно 2000 (стр. с 0 по 19 вкл. по 100)'''

    def check_connection(self) -> int:
        '''функция для проверки статус-кода при работе с API'''
        response = requests.get('https://api.hh.ru/vacancies')
        return response.status_code

    def get_vacancies(self, search_query: str) -> list:
        '''обращается к API и выгружает список вакансии согласно запросу search_query'''
        data = []
        params = {
            'text': search_query,
            'per_page': 100,
            'only_with_salary': True,
            'period': 30
        }
        while True:
            raw_data = requests.get('https://api.hh.ru/vacancies', params=params).json()
            page = raw_data['page']
            pages = raw_data['pages']
            data.extend(raw_data['items'])
            if page >= pages - 1:
                break
            params['page'] = page + 1
        return data

    def initialize_vacancy(self, search_query: str) -> None:
        '''для каждой вакансии, найденной по запросу search_query, инициализирует экземпляр Vacancy'''
        for i in self.get_vacancies(search_query):
            Vacancy(
                'HeadHunter',
                i['name'],
                i['area']['name'],
                i['employer']['name'],
                i['alternate_url'],
                int(i['salary']['from']) if i['salary']['from'] else 0,
                int(i['salary']['to']) if i['salary']['to'] else 0,
                i['salary']['currency'] if i['salary']['currency'] else None,
                i['snippet']['responsibility'] if i['snippet']['responsibility'] else None,
                i['snippet']['requirement'] if i['snippet']['requirement'] else None
            )


class SuperJobAPI(AbstractAPI):
    '''Максимальное количество сущностей, выдаваемых API равно 500 (стр. с 0 по 5 вкл. по 100)'''

    def check_connection(self) -> int:
        '''функция для проверки статус-кода при работе с API'''
        response = requests.get('https://api.superjob.ru')
        return response.status_code

    def get_vacancies(self, search_query: str) -> list:
        '''обращается к API и выгружает список вакансии согласно запросу search_query'''
        data = []
        search_from_date = datetime.datetime.now() - datetime.timedelta(days=30)
        search_from_date_unix = search_from_date.timestamp()
        headers = {'X-Api-App-Id': SJ_API_KEY}
        params = {
            'keyword': search_query,
            'count': 100,
            'page': 0,
            'no_agreement': 1,
            'date_published_from': search_from_date_unix
        }
        while True:
            raw_data = requests.get('https://api.superjob.ru/2.0/vacancies/', params=params, headers=headers).json()
            data.extend(raw_data['objects'])
            page = params['page']
            if not raw_data['more']:
                break
            params['page'] = page + 1
        return data

    def initialize_vacancy(self, search_query: str) -> None:
        '''для каждой вакансии, найденной по запросу search_query, инициализирует экземпляр Vacancy'''
        for i in self.get_vacancies(search_query):
            Vacancy(
                'SuperJob',
                i['profession'],
                i['town']['title'],
                i['firm_name'],
                i['link'],
                i['payment_from'],
                i['payment_to'],
                i['currency'],
                i['work'],
                i['candidat']
            )
