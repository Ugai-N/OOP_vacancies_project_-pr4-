import json
import os

import requests

from src.API import HeadHunterAPI, SuperJobAPI

CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')


class Vacancy:
    """класс для работы с вакансиями.
    Поддерживает методы сравнения вакансий между собой по зарплате и валидирует данные,
    которыми инициализируются его атрибуты"""

    vacancies_list = []

    def __init__(self, platform, title, area, company, url,
                 salary_min, salary_max, currency,
                 description, requirements):
        self.platform = platform
        self.title = title
        self.area = area
        self.company = company
        self.url = url
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = self.format_currency(currency)
        self.__salary_avr_rub = self.calc_salary(self.salary_min, self.salary_max, self.currency)
        self.description = description
        self.requirements = requirements
        Vacancy.vacancies_list.append(self)

    @property
    def salary_avr_rub(self):
        """Геттер для приватного атрибута __salary_avr_rub"""
        return self.__salary_avr_rub

    def __repr__(self):
        """Возвращает инфо в формате
        'Vacancy(<num>, <title>, <area>, зп: от <salary_min> до <salary_max> <currency>, <company>)'"""
        return f"{self.__class__.__name__} " \
               f"(поз.{Vacancy.vacancies_list.index(self)}, " \
               f"{self.title}, {self.area}, зп: от {self.salary_min} до {self.salary_max} {self.currency}, " \
               f"{self.company}\n)"

    def __str__(self):
        """Возвращает инфо в формате:
        '№<num>: <title>,
        Город: <area>,
        Компания: <company>,
        ЗП: от <salary_min> до <salary_max> <currency>,
        Ссылка: <url>,
        <description>,
        <requirements>'"""
        return f"№{Vacancy.vacancies_list.index(self) + 1}: " \
               f"{self.title},\n" \
               f"Город: {self.area},\n" \
               f"Компания: {self.company}, \n" \
               f"ЗП: от {self.salary_min} до {self.salary_max} {self.currency},\n" \
               f"Платформа: {self.platform}\n" \
               f"Ссылка: {self.url},\n" \
               f"{self.description},\n" \
               f"{self.requirements}\n\n"

    def __lt__(self, other):
        """Проверяет кол-во ЗП по первой вакансии < второй"""
        if isinstance(other, Vacancy):
            return int(self.salary_avr_rub) < int(other.salary_avr_rub)
        raise AttributeError('сравнение по ЗП возможно только между Вакансиями')

    @staticmethod
    def calc_salary(salary_min, salary_max, currency):
        """Возвращает среднее значение ЗП, если  определены мин и макс. Если нет - возвращает то, ктр определено"""
        if salary_min == 0:
            return Vacancy.exchange_currency(salary_max, currency)
        elif salary_max == 0:
            return Vacancy.exchange_currency(salary_min, currency)
        else:
            avr_original = (int(salary_min) + int(salary_max)) / 2
            return Vacancy.exchange_currency(avr_original, currency)

    @staticmethod
    def exchange_currency(amount, from_):
        """Возвращает размер ЗП с учетом пересчета в рубли по текущему курсу"""
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={from_}&amount={amount}"
        headers = {"apikey": CURRENCY_API_KEY}

        if amount > 0:
            response = requests.get(url, headers=headers)
            status_code = response.status_code
            data = json.loads(response.text)
            return int(data['result'])
            # if from_ == 'AZN':
            #     return amount * 57.25
            # elif from_ == 'BYR':
            #     return amount * 38.56
            # elif from_ == 'EUR':
            #     return amount * 106.68
            # elif from_ == 'USD':
            #     return amount * 99.25
            # elif from_ == 'GEL':
            #     return amount * 37.37
            # elif from_ == 'KGS':
            #     return amount * 1.11
            # elif from_ == 'KZT':
            #     return amount * 0.22
            # elif from_ == 'RUB':
            #     return amount
            # elif from_ == 'UAH':
            #     return amount * 2.65
            # elif from_ == 'UZS':
            #     return amount * 0.0083

    @staticmethod
    def format_currency(currency):
        """Форматирует наименование валюты, приводя к единым значениям и формату"""
        if currency == 'rub' or currency == 'RUR':
            return 'RUB'
        else:
            return currency.upper()


class HeadHunterVacancy(Vacancy):
    """Дочерний класс Vacancy для работы с платформой HeadHunter"""

    @classmethod
    def initialize_vacancy(cls, search_query: str) -> None:
        """для каждой вакансии, найденной по запросу search_query, инициализирует экземпляр Vacancy"""
        for i in HeadHunterAPI().get_vacancies(search_query):
            cls(
                'HeadHunter',
                i['name'],
                i['area']['name'],
                i['employer']['name'],
                i['alternate_url'],
                int(i['salary']['from']) if i['salary']['from'] else 0,
                int(i['salary']['to']) if i['salary']['to'] else 0,
                i['salary']['currency'] if i['salary']['currency'] else None,
                i['snippet']['responsibility'].strip() if i['snippet']['responsibility'] else None,
                i['snippet']['requirement'].strip() if i['snippet']['requirement'] else None
            )


class SuperJobVacancy(Vacancy):
    """Дочерний класс Vacancy для работы с платформой SuperJob"""

    @classmethod
    def initialize_vacancy(cls, search_query: str) -> None:
        """для каждой вакансии, найденной по запросу search_query, инициализирует экземпляр Vacancy"""
        for i in SuperJobAPI().get_vacancies(search_query):
            cls(
                'SuperJob',
                i['profession'],
                i['town']['title'],
                i['firm_name'],
                i['link'],
                i['payment_from'],
                i['payment_to'],
                i['currency'],
                i['work'].replace('\n', '\t') if i['work'] else None,
                i['candidat'].replace('\n', '\t') if i['candidat'] else None
            )
