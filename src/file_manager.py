from abc import ABC, abstractmethod


class AbstractFile(ABC):
    '''абстрактный класс, вкл методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и
    удаления информации о вакансиях'''

    @abstractmethod
    def save_vacancy(self):
        pass

    def get_vacancy(self):
        pass

    def del_vacancy(self):
        pass


class JsonFile(AbstractFile):
    '''класс для работы с вакансиями в JSON-файле'''

    def save_vacancy(self):
        pass

    def get_vacancy(self):
        pass

    def del_vacancy(self):
        pass


class ExcelFile(AbstractFile):
    '''класс для работы с вакансиями в Excel-файле'''

    def save_vacancy(self):
        pass

    def get_vacancy(self):
        pass

    def del_vacancy(self):
        pass
