import json
import os

import requests

CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')


class Vacancy:
    '''класс для работы с вакансиями.
    Поддерживает методы сравнения вакансий между собой по зарплате и валидирует данные,
    которыми инициализируются его атрибуты'''

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
        self.salary_avr_rub = self.calc_salary(self.salary_min, self.salary_max, self.currency)
        self.description = description
        self.requirements = requirements
        Vacancy.vacancies_list.append(self)

    def __repr__(self):
        return f"{self.__class__.__name__} " \
               f"(поз.{Vacancy.vacancies_list.index(self)}, " \
               f"{self.title}, {self.area}, зп: от {self.salary_min} до {self.salary_max} {self.currency}, " \
               f"{self.company}\n)"

    def __str__(self):
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
        '''Проверяет кол-во ЗП по первой вакансии < второй'''
        if isinstance(other, Vacancy):
            return int(self.salary_avr_rub) < int(other.salary_avr_rub)
        raise AttributeError('сравнение по ЗП возможно только между Вакансиями')

    @staticmethod
    def calc_salary(salary_min, salary_max, currency):
        '''Возвращает среднее значение ЗП, если  определены мин и макс. Если нет - возвращает то, ктр определено'''
        if salary_min == 0:
            # return salary_max
            return Vacancy.exchange_currency(salary_max, currency)
        elif salary_max == 0:
            # return salary_min
            return Vacancy.exchange_currency(salary_min, currency)
        else:
            avr_original = (int(salary_min) + int(salary_max)) / 2
            # return avr_original
            return Vacancy.exchange_currency(avr_original, currency)

    @staticmethod
    def exchange_currency(amount, from_):
        '''Возвращает размер ЗП с учетом пересчет в рубли по текущему курсу'''
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={from_}&amount={amount}"
        headers = {"apikey": CURRENCY_API_KEY}

        if amount > 0:
            response = requests.get(url, headers=headers)
            status_code = response.status_code
            data = json.loads(response.text)
            # print(status_code)
            return int(data['result'])

    @staticmethod
    def format_currency(currency):
        '''Форматирует наименование валюты, приводя к единым значениям'''
        if currency == 'rub' or currency == 'RUR':
            return 'RUB'
        else:
            return currency.upper()
