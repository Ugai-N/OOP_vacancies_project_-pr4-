# Script for searching job vacancies at platforms "HeadHunter" & "SuperJob" upon the user's request

# General:

* The search results are subject to the limits set by platforms: HeadHunter - 2000 vacancies, SuperJob - 500 vacancies
* Search results end into initialization of Vacancy class objects and are saved into JSON file

# Optional functions:

* Opportunity to filter the vacancies as per the salary amount 
* Opportunity to sort as per salary (ascending & descending) 
* Input of results qty to be included in TOP-results
* Choosing of console printing or saving to CSV-file (user file version)


Note: filtering and further sorting is performed in accordance to the current currency exchange rate via https://apilayer.com/


# Программа, реализующая поиск вакансий на платформах "HeadHunter" и "SuperJob" по запросу пользователя

# Общее:

* Поиск осуществляется с учетом ограничений по выгрузке вакансий в количестве: HeadHunter - 2000 вакансий, SuperJob - 500 вакансий
* По результатам поиска инициализируются экземпляры класса Vacancy и записываются в файл json

# Опциональный функционал:

* Фильтрация результатов поиска по заработной плате 
* Сортировка по ЗП, по возрастанию и убыванию 
* Ввод кол-ва вакансий, подлежащих включению в ТОП
* Вывод на печать в консоль результатов или в файл json  для пользователя


Прим. фильтрация и дальнейшая сортировка осуществляются с учетом текущего курса валюты вакансии к рублю через https://apilayer.com/
