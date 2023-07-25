import csv
import json
import os
import pandas as pd
from abc import ABC, abstractmethod

from pandas import ExcelWriter


class AbstractFile(ABC):
    '''абстрактный класс, вкл методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и
    удаления информации о вакансиях'''

    @abstractmethod
    def save_vacancy(self, file, vacancy):
        '''Сохраняет/добавляет в файл значения атрибутов экземпляра Vacancy'''
        pass

    @abstractmethod
    def get_vacancy(self, file, *keyword):
        '''Возвращает список вакансий из указанного файла, содержащих искомые слова'''
        pass

    @abstractmethod
    def del_vacancy(self, file, num):
        '''Удаляет вакансию из указанного файла по номеру вакансии'''
        pass


class JsonFile(AbstractFile):
    '''класс для работы с вакансиями в JSON-файле'''

    def save_vacancy(self, file, vacancy_list) -> None:
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
                    "Валюта": vacancy.currency,
                    "Зарплата (среднее, RUB)": vacancy.salary_avr_rub,
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

    def get_vacancy(self, file, *keyword) -> list:
        '''Возвращает список вакансий из указанного файла, содержащих искомые слова'''
        filtered_lst = []
        with open(file, 'r', encoding='utf-8') as f:
            vacancies_filelist = json.load(f)
            for vacancy in vacancies_filelist:
                for word in keyword:
                    if word in vacancy.values():
                        filtered_lst.append(vacancy)
        return filtered_lst

    def del_vacancy(self, file, num) -> None:
        '''Удаляет вакансию из указанного файла по номеру вакансии'''
        with open(file, 'r', encoding='utf-8') as f:
            vacancies_filelist = json.load(f)
            for vacancy in vacancies_filelist:
                if vacancy['№'] == int(num):
                    vacancies_filelist.remove(vacancy)
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(vacancies_filelist, f, ensure_ascii=False)


# class ExcelFile(AbstractFile):
#     '''класс для работы с вакансиями в Excel-файле'''
#
#     def save_vacancy(self, file, vacancy_list) -> None:
#         vacancy_csv_list = []
#         for vacancy in vacancy_list:
#             vacancy_data = []
#             vacancy_data.append(vacancy_list.index(vacancy) + 1),
#             vacancy_data.append(vacancy.title),
#             vacancy_data.append(vacancy.area),
#             vacancy_data.append(vacancy.company),
#             vacancy_data.append(vacancy.platform),
#             vacancy_data.append(vacancy.url),
#             vacancy_data.append(vacancy.salary_min),
#             vacancy_data.append(vacancy.salary_max),
#             vacancy_data.append(vacancy.salary_avr_rub),
#             vacancy_data.append(vacancy.currency),
#             vacancy_data.append(vacancy.description),
#             vacancy_data.append(vacancy.requirements)
#             vacancy_csv_list.append(vacancy_data)
#         csv_columns = ['№', 'Вакансия', 'Регион', 'Компания', 'Платформа', 'Ссылка',
#                        'Зарплата от', 'Зарплата до', 'Валюта', 'Зарплата (среднее, RUB)', 'Описание', 'Требования']
#         data = pd.DataFrame(vacancy_csv_list, columns=csv_columns)
#         data.to_csv(file, encoding='utf-8-sig', index=False)


    # def save_vacancy(self, file, vacancy_list) -> None:
        #
        # excel_dict = {'Вакансия': [],
        #               'Регион': [],
        #               'Компания': [],
        #               'Платформа': [],
        #               'Ссылка': [],
        #               'Зарплата от': [],
        #               'Зарплата до': [],
        #               'Валюта': [],
        #               'Зарплата (среднее, RUB)': [],
        #               'Описание': [],
        #               'Требования': []
        #               }
        # for vacancy in vacancy_list:
        #     # excel_dict['Вакансия'].append(f'{vacancy.title!r}') - может ли быть ошибка записи файла, т.к. нет кавычек?
        #     excel_dict['Вакансия'].append(vacancy.title),
        #     excel_dict['Регион'].append(vacancy.area),
        #     excel_dict['Компания'].append(vacancy.company),
        #     excel_dict['Платформа'].append(vacancy.platform),
        #     excel_dict['Ссылка'].append(vacancy.url),
        #     excel_dict['Зарплата от'].append(vacancy.salary_min),
        #     excel_dict['Зарплата до'].append(vacancy.salary_max),
        #     excel_dict['Зарплата (среднее, RUB)'].append(vacancy.salary_avr_rub),
        #     excel_dict['Валюта'].append(vacancy.currency),
        #     excel_dict['Описание'].append(vacancy.description),
        #     excel_dict['Требования'].append(vacancy.requirements)
        #
        # data = pd.DataFrame(excel_dict)
        # with ExcelWriter(file, mode="a" if os.path.exists(file) else "w") as writer:
        #     data.to_excel(writer, sheet_name='vacancies', index=False)
        # data.to_excel(file, sheet_name='vacancies', index=False)
    #
    # def get_vacancy(self, file, *keyword) -> list:
    #     '''черновик, не могу проверить пока'''
    #     filtered_lst = []
    #     excel_data = pd.read_excel(file)
    #     data = pd.DataFrame(excel_data, columns=['Вакансия', 'Регион', 'Компания', 'Платформа',
    #                                              'Ссылка', 'Зарплата от', 'Зарплата до',
    #                                              'Зарплата, среднее значение', 'Валюта',
    #                                              'Описание', 'Требования'])
    #     for vacancy in data:
    #         for word in keyword:
    #             if word in vacancy.values():
    #                 filtered_lst.append(vacancy)
    #     return filtered_lst
    #
    # def del_vacancy(self, file, num) -> None:
    #     '''черновик, не могу проверить пока'''
    #     data = pd.read_excel(file)
    #     del_index = data.set_index('№')
    #     del_index.drop([int(num)], axis=0)
