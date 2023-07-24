from pathlib import Path

from src.file_manager import JsonFile
from src.utils import choose_platform, choose_filter, choose_sorting, choose_top_qty, deliver_results, stop_list, \
    print_results
from src.vacancy import Vacancy
# print(Vacancy.exchange_currency(10/3, 'RUB'))

# fff_path = Path(__file__).resolve().parent.joinpath('data','_Nadya_python.json')
# print(JsonFile().del_vacancy(fff_path, 10))
# print_results(JsonFile().get_vacancy(fff_path, 'Петрозаводск', 'СОШ'))

user_name = input('Привет! я могу помочь в поиске вакансий '
                  'на платформах "HeadHunter" и "SuperJob". '
                  'Напишите свое имя:\n')
user_name_upd = ''.join(symbol for symbol in user_name if symbol.isalnum())[:10]
results = Vacancy.vacancies_list.clear()
while True:
    search_query = input("Введите поисковый запрос: ")
    search_query_upd = ''.join(symbol for symbol in search_query if symbol.isalnum())[:10]
    file_path = Path(__file__).resolve().parent.joinpath('data',
                                                         f'_{str(user_name_upd)}_'
                                                         f'{str(search_query_upd)}'
                                                         f'.json')
    user_file_path_xsl = Path(__file__).resolve().parent.joinpath('data',
                                                                  f'{str(user_name_upd)}_'
                                                                  f'{str(search_query_upd)}'
                                                                  f'.xlsx')

    results = choose_platform(search_query)
    if len(results) != 0:
        print(f'Нашли {len(results)} вакансий')
    else:
        print('По вашему запросу ничего не найдено. Попробуйте еще раз')
        continue
    # for i in results:
    #     print(i.currency)

    JsonFile().save_vacancy(file_path, results)
    results = choose_filter(results)
    if len(results) != 0:
        print(f'После фильтрации нашли {len(results)} вакансий')
    else:
        print('По вашему запросу ничего не найдено. Попробуйте еще раз')
        continue
    results = choose_sorting(results)
    results = choose_top_qty(results)
    deliver_results(results, user_file_path_xsl)

    to_continue = input('Хотите начать поиск сначала или выйти?\n'
                        '1 - СНАЧАЛА\n'
                        '2 - ВЫЙТИ\n')
    if to_continue == '1':
        continue
    elif to_continue == '2':
        break
