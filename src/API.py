from abc import ABC, abstractmethod

import requests

from src.vacancy import Vacancy


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
    def check_connection(self) -> int:
        response = requests.get('https://api.hh.ru/vacancies')
        return response.status_code

    def get_vacancies(self, search_query: str) -> list:
        data = []
        for page in range(0, 20):
            params = {
                      'text': search_query,
                      'page': page,
                      'per_page': 10
                     }
            raw_data = requests.get('https://api.hh.ru/vacancies', params=params).json()
            data.extend(raw_data['items'])
        return data

    @staticmethod
    def qty_vacancies(self, search_query: str) -> str:
        params = {
                  'text': search_query,
                  'per_page': 100
                 }
        raw_data = requests.get('https://api.hh.ru/vacancies', params=params).json()
        return f"По запросу '{search_query}' найдено {raw_data['found']} вакансий, возможно отразить только 2000"

    def initialize_vacancy(self, search_query: str) -> None:
        for i in self.get_vacancies(search_query):
            Vacancy(i['name'], i['area']['name'], i['alternate_url'], i['salary'], i['snippet'])


class SuperJobAPI(AbstractAPI):
    def check_connection(self) -> int:
        pass

    def get_vacancies(self, search_query: str) -> list:
        pass

    def initialize_vacancy(self, search_query: str) -> None:
        pass
