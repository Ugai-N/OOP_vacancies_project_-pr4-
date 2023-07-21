
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
        self.salary_avr = self.calc_salary(salary_min, salary_max)
        self.currency = currency
        self.description = description
        self.requirements = requirements
        Vacancy.vacancies_list.append(self)

    def __repr__(self):
        return f"{self.__class__.__name__} " \
               f"(поз.{Vacancy.vacancies_list.index(self)}, " \
               f"{self.title}, {self.area}, зп: от {self.salary_min} до {self.salary_max} {self.currency}, " \
               f"{self.company}\n)"

    def __str__(self):
        return f"{Vacancy.vacancies_list.index(self) + 1}," \
               f"{self.title},\n" \
               f"Город: {self.area},\n" \
               f"Компания: {self.company}, \n" \
               f"ЗП: от {self.salary_min} до {self.salary_max} {self.currency},\n" \
               f"Платформа: \n" \
               f"Ссылка: {self.url},\n" \
               f"{self.description},\n" \
               f"{self.requirements}\n\n"

    def __lt__(self, other):
        '''Проверяет кол-во ЗП по первой вакансии < второй'''
        if isinstance(other, Vacancy):
            # if self.currency == other.currency:
            return int(self.salary_avr) < int(other.salary_avr)
            # pass
        raise AttributeError('сравнение по ЗП возможно только между Вакансиями')

    @staticmethod
    def calc_salary(salary_min, salary_max):
        if salary_min == 0:
            return salary_max
        elif salary_max == 0:
            return salary_min
        else:
            return (int(salary_min) + int(salary_max)) / 2
