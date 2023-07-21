from src.vacancy import Vacancy


def filter_by_salary(salary_from, salary_to):
    filtered_list = []
    for i in Vacancy.vacancies_list:
        if int(salary_from) <= int(i.salary_min) <= int(salary_to) or \
                int(salary_from) <= int(i.salary_max) <= int(salary_to):
            filtered_list.append(i)
    return filtered_list


def sort_by_salary_up(results):
    '''начала низкие'''
    sorted_results = sorted(results)
    return sorted_results


def sort_by_salary_down(results):
    '''начала высокие'''
    sorted_results = sorted(results, reverse=True)
    return sorted_results


def get_top_vacancies(vacancies, qty):
    return vacancies[:qty]


def print_results(results):
    for vacancy in results:
        print(vacancy)
