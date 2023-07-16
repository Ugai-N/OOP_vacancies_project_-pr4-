from src.API import HeadHunterAPI, SuperJobApi

hh_vacancies = HeadHunterAPI.get_vacancies()
sj_vacancies = SuperJobApi.get_vacancies()


def filter_vacancies(hh_vacancies, sj_vacancies, filter_words):
    pass


def sort_vacancies(vacancies):
    pass


def get_top_vacancies(vacancies, qty):
    pass


def print_vacancies(info):
    pass


def user_interaction():
    platforms = ["HeadHunter", "SuperJob"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filtered_vacancies = filter_vacancies(hh_vacancies, sj_vacancies, filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()