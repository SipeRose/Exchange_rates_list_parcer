import re
import mechanicalsoup
import sqlite3
import Dictionary
import SQL_commands
import URLs


class RelativeUpdater:  # Класс для работы с относительными изменениями курсов

    def __init__(self):
        self.url = URLs.url3  # Курсы за конкретную дату для всех стран берутся с вкладки "Все курсы на дату"
        # сайта Финмаркет
        self.data_list = {}  # Словарь будет содержать курсы валют на выбранную дату
        self.day = '1'  # По умолчанию заданная дата, с которой сравнивают курсы
        self.month = 'сентября'
        self.year = '2023'

    def new_date(self, new_day, new_month, new_year):  # Выбор новой заданной даты, с которой сравнивают курсы
        self.day = new_day
        self.month = new_month
        self.year = new_year

        with sqlite3.connect("data_base.db") as connection:  # Удаление старой даты из таблицы
            cursor = connection.cursor()
            cursor.execute('DROP TABLE Relative_change')

        self.add_to_data_base()  # Новые относительные изменения
        self.add_date_to_parameters()

    def add_date_to_parameters(self):  # Вставка новой даты в таблицу параметров

        day = self.day + ' ' + self.month + ' ' + self.year

        with sqlite3.connect('data_base.db') as connection:
            cursor = connection.cursor()
            cursor.executescript(SQL_commands.create_table_Parameters_table)
            cursor.execute('INSERT INTO Parameters_table VALUES(?);', (day,))

    def add_to_data_base(self):  # Вставка относительных изменений курса в таблицу

        html_code = self.get_html(self.day, self.month, self.year)
        self.get_data_from_html(html_code)

        with sqlite3.connect('data_base.db') as connection:
            cursor = connection.cursor()
            cursor.execute(SQL_commands.create_table_Relative_change)
            for element in self.data_list:
                cursor.execute(SQL_commands.insert_into_table_Relative_change, (self.data_list[element], element))

    @staticmethod
    def decoder(browser, encoding):  # Декодер для HTML, на вход: browser - объект mechanicalsoup.StatefulBrowser(),
        # encoding - кодировка

        return (browser.page.decode(encoding).replace('\n', '')).replace(' ', '')

    def get_html(self, day, month, year):  # Получение HTML-кода страницы

        browser = mechanicalsoup.StatefulBrowser()
        browser.open(self.url)
        browser.select_form('form[action="/currency/rates/#archive"]')
        browser["bd"] = day  # Выбор нужного тэга option по атрибуту
        browser["bm"] = Dictionary.months_values[month]
        browser["by"] = year
        browser.submit_selected()

        return self.decoder(browser, 'windows-1251')

    def get_data_from_html(self, html_code):  # Поиск курса валют в HTML-коде с помощью регулярных выражений

        for currency in Dictionary.Currencies:  # Для всех валют из словаря
            new_currency = currency.replace(' ', '')
            try:
                data = re.findall(f'{new_currency}.*?,.*?</td>', html_code)[0]
                data = re.sub('.*?[01]</td><td>', '', data)
                data = re.sub('</td>', '', data)
                data = data.replace(',', '.')
            except IndexError:  # Для некоторых валют бывает отсутствие данных, которое обрабатывается этим блоком
                print(f'Для валюты {currency} нет данных. Присвоено значение 1')
                data = '1'
            self.data_list[currency] = data
