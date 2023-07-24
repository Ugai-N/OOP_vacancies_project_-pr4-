import sys

from src.API import HeadHunterAPI, SuperJobAPI
from src.file_manager import JsonFile
from src.vacancy import Vacancy
stop_list = ['stop', 'стоп', 'выйти', 'выход', 'exit', 'quit']


def choose_platform(search_query, platform_search='ok') -> list:
    '''Взаимодействие с пользователем по выбору платформы. Возвращает список экземпляров класса Vacancy.
    Прекращает выполнение программы при вводе включевых слов их stop_list'''
    while platform_search.lower() not in stop_list:
        platform_search = input("Выберите платформу для поиска вакансий:\n"
                                "1 - 'HeadHunter'\n"
                                "2 - 'SuperJob'\n"
                                "3 - 'ОБЕ'\n")
        if platform_search == '1':
            HeadHunterAPI().initialize_vacancy(search_query)
            return Vacancy.vacancies_list
        elif platform_search == '2':
            SuperJobAPI().initialize_vacancy(search_query)
            return Vacancy.vacancies_list
        elif platform_search == '3':
            HeadHunterAPI().initialize_vacancy(search_query)
            SuperJobAPI().initialize_vacancy(search_query)
            return Vacancy.vacancies_list
    sys.exit()


def choose_filter(results, to_filter='ok') -> list:
    '''Взаимодействие с пользователем по выбору фильтра. Возвращает список экземпляров класса Vacancy,
    запуская filter_by_salary(). Прекращает выполнение программы при вводе включевых слов их stop_list'''
    while to_filter.lower() not in stop_list:
        to_filter = input('Хотите ли вы дополнительно отфильтровать полученные результаты по ЗП?\n'
                          '1 - ДА\n'
                          '2 - НЕТ\n')
        if to_filter == '1':
            while True:
                salary_from = input('Укажите нижнюю границу по ЗП цифрами?\n').replace(' ', '')
                if salary_from.isdigit():
                    break
                print('На ввод допускаются только цифры. Попробуйте еще раз')
                continue
            while True:
                salary_to = input('Укажите верхнюю границу по ЗП цифрами?\n').replace(' ', '')
                if salary_to.isdigit():
                    if int(salary_to) >= int(salary_from):
                        return filter_by_salary(salary_from, salary_to)
                    print('Введенная верхняя граница ниже установленной нижней. Попробуйте еще раз')
                    continue
                print('На ввод допускаются только цифры. Попробуйте еще раз')
                continue
        elif to_filter == '2':
            return results
    sys.exit()


def filter_by_salary(salary_from, salary_to) -> list:
    '''Проверяет вхождение мин и макс ЗП в установленные граница поиска'''
    filtered_list = []
    for i in Vacancy.vacancies_list:
        if int(salary_from) <= int(i.salary_min) <= int(salary_to) or \
                int(salary_from) <= int(i.salary_max) <= int(salary_to):
            filtered_list.append(i)
    return filtered_list


def choose_sorting(results, sort_by_salary='ok') -> list:
    '''Взаимодействие с пользователем по сортировке. Возвращает список экземпляров класса Vacancy,
    запуская sort_by_salary_up() или sort_by_salary_down().
    Прекращает выполнение программы при вводе включевых слов их stop_list'''
    while sort_by_salary.lower() not in stop_list:
        sort_by_salary = input('Хотите ли вы отсортировать полученные результаты по ЗП?\n'
                               '1 - СНАЧАЛА ВЫСОКИЕ\n'
                               '2 - СНАЧАЛА НИЗКИЕ\n'
                               '3 - СОРТИРОВКА НЕ НУЖНА\n')
        if sort_by_salary == '1':
            return sort_by_salary_down(results)
        elif sort_by_salary == '2':
            return sort_by_salary_up(results)
        elif sort_by_salary == '3':
            return results
    sys.exit()


def sort_by_salary_up(results) -> list:
    '''Сортирует по принципу: сначала низкие'''
    sorted_results = sorted(results)
    return sorted_results


def sort_by_salary_down(results) -> list:
    '''Сортирует по принципу: сначала высокие'''
    sorted_results = sorted(results, reverse=True)
    return sorted_results


def choose_top_qty(results, top_results='ok') -> list:
    '''Взаимодействие с пользователем по определению кол-ва вакансий в топе.
    Возвращает список экземпляров класса Vacancy, запуская get_top_vacancies().
    Прекращает выполнение программы при вводе включевых слов их stop_list'''
    while top_results.lower() not in stop_list:
        top_results = input('Введите количество вакансий для вывода в топ?\n')
        if top_results.isdigit():
            return get_top_vacancies(results, int(top_results))
        print('На ввод допускаются только цифры. Попробуйте еще раз')
        continue
    sys.exit()


def get_top_vacancies(vacancies, qty) -> list:
    '''Возвращает первые вакансии в списки в коливестве qty'''
    return vacancies[:qty]


def deliver_results(results, path):
    '''Взаимодействие с пользователем по выбору метода печати результатов'''
    deliver_method = input('Вывести результаты на экран или сохранить в файл EXCEL?\n'
                           '1 - ВЫВЕСТИ НА ЭКРАН\n'
                           '2 - EXCEL\n')
    if deliver_method == '1':
        print_results(results)
    elif deliver_method == '2':
        JsonFile().save_vacancy(path, results)
        print(f'Ваши результаты сохранены в файл по указанному пути: {path}')


def print_results(results):
    '''Функция вывода на печать в консоль'''
    for vacancy in results:
        print(vacancy)
