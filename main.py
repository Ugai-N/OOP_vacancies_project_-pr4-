from pathlib import Path

from src.API import HeadHunterAPI, SuperJobAPI
from src.file_manager import JsonFile
from src.utils import filter_by_salary, sort_by_salary_up, sort_by_salary_down, get_top_vacancies, print_results
from src.vacancy import Vacancy

#
# plumber.initialize_vacancy('python')
# lst = Vacancy.vacancies_list.copy()
# # sort_by_salary_up(lst)
# print(len(lst))
# for i in lst:
#     if isinstance(i, Vacancy):
#         pass
#     else:
#         print('oo')
# print(sort_by_salary_up(lst))


request_num = 6
results = []
while True:
    '''Может добавить опцию 0 для выхода?'''

    Vacancy.vacancies_list.clear()
    file_path = Path(__file__).resolve().parent.joinpath('data', str(request_num) + '.json')
    user_file_path_js = Path(__file__).resolve().parent.joinpath('data', str(request_num) + 'user' + '.json')
    user_file_path_xsl = Path(__file__).resolve().parent.joinpath('data', str(request_num) + 'user' + '.xlsx')
    search_query = input("Введите поисковый запрос: ")
    platform_search = input("Выберите платформу для поиска вакансий:\n"
                            "1 - 'HeadHunter'\n"
                            "2 - 'SuperJob'\n"
                            "3 - 'ОБЕ'\n")
    print('Уже ищем. Секундочку')
    if platform_search == '1':
        HeadHunterAPI().initialize_vacancy(search_query)
    elif platform_search == '2':
        SuperJobAPI().initialize_vacancy(search_query)
    elif platform_search == '3':
        HeadHunterAPI().initialize_vacancy(search_query)
        SuperJobAPI().initialize_vacancy(search_query)
    else:
        print('Такой опции у нас нет. Попробуйте еще раз')
        break

    results = Vacancy.vacancies_list
    print(f'Нашли {len(results)} вакансий и записываем в общ.файл')
    JsonFile().save_vacancy(file_path, Vacancy.vacancies_list)

    while True:
        to_filter = input('Хотите ли вы дополнительно отфильтровать полученные результаты по ЗП?\n'
                          '1 - ДА\n'
                          '2 - НЕТ\n')
        if to_filter == '1':
            while True:
                salary_from = input('Укажите нижнюю границу по ЗП цифрами?\n').replace(' ', '')
                if salary_from.isdigit():
                    break
                else:
                    print('На ввод допускаются только цифры. Попробуйте еще раз')
                    continue
            while True:
                salary_to = input('Укажите верхнюю границу по ЗП цифрами?\n').replace(' ', '')
                if salary_to.isdigit():
                    results = filter_by_salary(salary_from, salary_to)
                    print(f'После фильтрации доступно {len(results)} вакансий')
                    break
                else:
                    print('На ввод допускаются только цифры. Попробуйте еще раз')
                    continue
            break
        elif to_filter == '2':
            break

    while True:
        sort_by_salary = input('Хотите ли вы отсортировать полученные результаты по ЗП?\n'
                               '1 - СНАЧАЛА ВЫСОКИЕ\n'
                               '2 - СНАЧАЛА НИЗКИЕ\n'
                               '3 - СОРТИРОВКА НЕ НУЖНА\n')
        if sort_by_salary == '1':
            results = sort_by_salary_down(results)
            print(results)
            break
        elif sort_by_salary == '2':
            results = sort_by_salary_up(results)
            print(results)
            break
        elif sort_by_salary == '3':
            break

    while True:
        top_results = input('Введите количество вакансий для вывода в топ?\n')
        if top_results.isdigit():
            results = get_top_vacancies(results, int(top_results))
            break
        else:
            print('На ввод допускаются только цифры. Попробуйте еще раз')
            continue

    while True:
        deliver_results = input('Вывести результаты на экран или сохранить в файл EXCEL?\n'
                                '1 - ВЫВЕСТИ НА ЭКРАН\n'
                                '2 - EXCEL\n')
        if deliver_results == '1':
            print_results(results)
            break
        elif deliver_results == '2':
            JsonFile().save_vacancy(user_file_path_xsl, results)
            print(f'Ваши результаты сохранены в файл по указанному пути: {user_file_path_xsl}')
            break

    to_continue = input('Хотите начать поиск сначала или выйти?\n'
                        '1 - СНАЧАЛА\n'
                        '2 - ВЫЙТИ\n')
    if to_continue == '1':
        request_num += 1
        continue
    elif to_continue == '2':
        break
