class Vacancy:
    '''класс для работы с вакансиями. Атрибуты: name, url, salary, requirements.
    Поддерживает методы сравнения вакансий между собой по зарплате и валидирует данные,
    которыми инициализируются его атрибуты'''

    def __init__(self, name, url, salary, requirements):
        self.name = name
        self.url = url
        self.salary = salary
        self.requirements = requirements
