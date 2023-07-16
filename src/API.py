import json
from abc import ABC, abstractmethod

import requests


class AbstractAPI(ABC):
    '''абстрактный класс для работы с API сайтов с вакансиями.
    Наследники класса для каждой платформы подключаются к API и получают вакансии'''

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(AbstractAPI):
    def get_vacancies(self):
        data = requests.get('https://api.hh.ru/vacancies').json()
        return data
        # return len(data['items'])
        # return data['found']


class SuperJobApi(AbstractAPI):
    def get_vacancies(self):
        pass
