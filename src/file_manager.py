import csv
import json
import os
from abc import ABC, abstractmethod


class AbstractFile(ABC):
    """абстрактный класс, вкл методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и
    удаления информации о вакансиях"""

    @abstractmethod
    def save_vacancy(self, file, vacancy):
        """Сохраняет/добавляет в файл значения атрибутов экземпляра Vacancy"""
        pass

    @abstractmethod
    def get_vacancy(self, file, *keyword):
        """Возвращает список вакансий из указанного файла, содержащих искомые слова"""
        pass

    @abstractmethod
    def del_vacancy(self, file, num):
        """Удаляет вакансию из указанного файла по номеру вакансии"""
        pass


class JsonFile(AbstractFile):
    """класс для работы с вакансиями в JSON-файле"""

    def save_vacancy(self, file, vacancy_list) -> None:
        """Сохраняет/добавляет в файл json значения атрибутов экземпляра Vacancy."""
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
        """Возвращает список вакансий из указанного json файла, содержащих искомые слова.
        Для унификации поиска все данные приведены в нижнем регистре"""
        filtered_lst = []
        with open(file, 'r', encoding='utf-8') as f:
            vacancies_filelist = json.load(f)
            for vacancy in vacancies_filelist:
                for word in keyword:
                    if word.lower() in ' '.join(str(i) for i in vacancy.values()).lower():
                        filtered_lst.append(vacancy)
        return filtered_lst

    def del_vacancy(self, file, num) -> None:
        """Удаляет вакансию из указанного json файла по номеру вакансии"""
        with open(file, 'r', encoding='utf-8') as f:
            vacancies_filelist = json.load(f)
            for vacancy in vacancies_filelist:
                if vacancy['№'] == int(num):
                    vacancies_filelist.remove(vacancy)
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(vacancies_filelist, f, ensure_ascii=False)


class CSVFile(AbstractFile):
    """класс для работы с вакансиями в CSV-файле"""

    def save_vacancy(self, file, vacancy_list) -> None:
        """Сохраняет/добавляет в файл csv значения атрибутов экземпляра Vacancy."""
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
        names = ["№",
                 "Вакансия",
                 "Регион",
                 "Компания",
                 "Платформа",
                 "Ссылка",
                 "Зарплата от",
                 "Зарплата до",
                 "Валюта",
                 "Зарплата (среднее, RUB)",
                 "Описание",
                 "Требования"]
        if os.path.exists(file):
            with open(file, mode="a", encoding='utf-8-sig') as w_file:
                file_writer = csv.DictWriter(w_file, delimiter=",",
                                             lineterminator="\r", fieldnames=names)
                file_writer.writerows(vacancies_dict_list)
        with open(file, mode="w", encoding='utf-8-sig') as w_file:
            file_writer = csv.DictWriter(w_file, delimiter=",",
                                         lineterminator="\r", fieldnames=names)
            file_writer.writeheader()
            file_writer.writerows(vacancies_dict_list)

    def get_vacancy(self, file, *keyword) -> list:
        """Возвращает список вакансий из указанного csv файла, содержащих искомые слова.
        Для унификации поиска все данные приведены в нижнем регистре"""
        filtered_lst = []
        with open(file, mode="r", newline='', encoding='utf-8-sig') as r_file:
            file_reader = csv.reader(r_file)
            for col in file_reader:
                for word in keyword:
                    if word.lower() in ', '.join(col[i] for i in range(1, 12)).lower():
                        filtered_lst.append(col)
        return filtered_lst

    def del_vacancy(self, file, num) -> None:
        """Удаляет вакансию из указанного csv файла по номеру вакансии
        ('этот вариант удаляет вакансию в изначальном файле. См альтернативный вариант - ниже)"""
        with open(file, mode="r", newline='', encoding='utf-8-sig') as source:
            file_reader = csv.DictReader(source)
            new_list = []
            for col in file_reader:
                if int(col["№"]) != int(num):
                    new_list.append(col)
        with open(file, mode="w", encoding='utf-8-sig') as destination:
            file_writer = csv.DictWriter(destination, delimiter=",",
                                         lineterminator="\r", fieldnames=file_reader.fieldnames)
            file_writer.writeheader()
            file_writer.writerows(new_list)
