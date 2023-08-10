from pathlib import Path

from src.file_manager import JsonFile
from src.utils import choose_platform, choose_filter, choose_sorting, choose_top_qty, deliver_results, print_results_qty
from src.vacancy import Vacancy

user_name = input('Привет! я могу помочь в поиске вакансий '
                  'на платформах "HeadHunter" и "SuperJob". \n'
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
    user_file_path_csv = Path(__file__).resolve().parent.joinpath('data',
                                                                  f'{str(user_name_upd)}_'
                                                                  f'{str(search_query_upd)}'
                                                                  f'.csv')
    results = choose_platform(search_query)
    print_results_qty(results)
    JsonFile().save_vacancy(file_path, results)
    results = choose_filter(results)
    print_results_qty(results)
    results = choose_sorting(results)
    results = choose_top_qty(results)
    deliver_results(results, user_file_path_csv)

    to_continue = input('Хотите начать поиск сначала или выйти?\n'
                        '1 - СНАЧАЛА\n'
                        '2 - ВЫЙТИ\n')
    if to_continue == '1':
        continue
    elif to_continue == '2':
        break
