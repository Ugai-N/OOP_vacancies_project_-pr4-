import json
import os
import pandas as pd
from abc import ABC, abstractmethod


class AbstractFile(ABC):
    '''абстрактный класс, вкл методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и
    удаления информации о вакансиях'''

    @abstractmethod
    def save_vacancy(self, file, vacancy):
        pass

    def get_vacancy(self):
        pass

    def del_vacancy(self):
        pass


class JsonFile(AbstractFile):
    '''класс для работы с вакансиями в JSON-файле'''

    def save_vacancy(self, file, vacancy_list):
        """Сохраняет/добавляет в файл значения атрибутов экземпляра Vacancy."""
        vacancies_dict_list = []
        for vacancy in vacancy_list:
            data = {"№": vacancy_list.index(vacancy) + 1,
                    "Вакансия": vacancy.title,
                    "Регион": vacancy.area,
                    "Компания": vacancy.company,
                    "Платформа": vacancy.platform,
                    "Ссылка": vacancy.url,
                    "Зарплата от": vacancy.salary_min,
                    "Зарплата до": vacancy.salary_max,
                    "Зарплата, среднее значение": vacancy.salary_avr,
                    "Валюта": vacancy.currency,
                    "Описание": vacancy.description,
                    "Требования": vacancy.requirements
                    }

            vacancies_dict_list.append(data)

        with open(file, 'a', encoding='utf-8') as f:
            if os.stat(file).st_size == 0:
                json.dump(vacancies_dict_list, f, ensure_ascii=False)
            else:
                with open(file, 'r', encoding='utf-8') as f:
                    vacancies_filelist = json.load(f)
                    vacancies_filelist += vacancies_dict_list
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump(vacancies_filelist, f, ensure_ascii=False)

    def get_vacancy(self):
        pass

    def del_vacancy(self):
        pass


class ExcelFile(AbstractFile):
    '''класс для работы с вакансиями в Excel-файле'''

    def save_vacancy(self, file, vacancy_list):
        excel_dict = {'Вакансия': [],
                      'Регион': [],
                      'Компания': [],
                      'Платформа': [],
                      'Ссылка': [],
                      'Зарплата от': [],
                      'Зарплата до': [],
                      'Зарплата, среднее значение': [],
                      'Валюта': [],
                      'Описание': [],
                      'Требования': []
                      }
        for vacancy in vacancy_list:
            # excel_dict['Вакансия'].append(f'{vacancy.title!r}'),
            excel_dict['Вакансия'].append(vacancy.title),
            excel_dict['Регион'].append(vacancy.area),
            excel_dict['Компания'].append(vacancy.company),
            excel_dict['Платформа'].append(vacancy.platform),
            excel_dict['Ссылка'].append(vacancy.url),
            excel_dict['Зарплата от'].append(vacancy.salary_min),
            excel_dict['Зарплата до'].append(vacancy.salary_max),
            excel_dict['Зарплата, среднее значение'].append(vacancy.salary_avr),
            excel_dict['Валюта'].append(vacancy.currency),
            excel_dict['Описание'].append(vacancy.description),
            excel_dict['Требования'].append(vacancy.requirements)

        data = pd.DataFrame(excel_dict)
        data.to_excel(file)

    def get_vacancy(self):
        pass

    def del_vacancy(self):
        pass
