import re
import mechanicalsoup
import sqlite3
import Dictionary
import SQL_commands
import URLs


class CurrencyReader:  # Класс для работы со списком курсов валют и списком стран

    def __init__(self):
        self.url1 = URLs.currency_url
        self.url2 = URLs.country_url

    def data_parser(self, first_day, first_month, first_year, last_day, last_month, last_year):  # парсер страницы, на
        # вход:начальная дата и конечная для считывания курсов. Здесь же и считыватель списка стран

        browser = mechanicalsoup.StatefulBrowser()
        browser.open(self.url1)  # Для списка курсов валют
        for currency in Dictionary.Currencies:  # Для каждой валюты
            browser.select_form('form[action="/currency/rates/#archive"]')
            browser["cur"] = Dictionary.Currencies[currency]  # Выбор нужного диапазона дат по значению атрибутов
            browser["bd"] = first_day
            browser["bm"] = Dictionary.months_values[first_month]
            browser["by"] = first_year
            browser["ed"] = last_day
            browser["em"] = Dictionary.months_values[last_month]
            browser["ey"] = last_year
            browser.submit_selected()
            data_list = self.get_data_from_html(browser, 'windows-1251')
            self.make_sql_for_currencies(currency, data_list)

        browser.open(self.url2)  # Для списка стран
        data_list = self.get_data_from_html(browser, 'utf-8')
        self.make_sql_for_countries(data_list)

    @staticmethod
    def decoder(browser, encoding):  # Декодер для HTML, на вход: browser - объект mechanicalsoup.StatefulBrowser(),
        # encoding - кодировка

        return ((browser.page.decode(encoding).replace('\n', '')).replace("\xa0", ''))  # replace(' ', '')).

    def get_data_from_html(self, browser, encoding):  # возвращает список тэгов с их текстом:
        # датой, курсом, количеством, изменением

        html_code = self.decoder(browser, encoding)
        pattern1 = '<tbody.*?>.*?</tbody>'
        pattern2 = '<td.*?>.*?</td>'
        data_list = re.findall(pattern1, html_code)  # поиск с помощью регулярных выражений

        return re.findall(pattern2, data_list[0])

    @staticmethod
    def change_date(date):  # Изменение даты на шаблон типа DATE SQL
        chaged_date = re.sub(' ', '', date)
        return chaged_date[6:] + '-' + chaged_date[3:5] + '-' + chaged_date[:2]

    @staticmethod
    def resub(string):  # Замена всех подстрок строки, соответствующих регулрному выражению, пустым символом

        return re.sub('<.*?>', "", string)

    def make_sql_for_currencies(self, currency, data_list):  # Чтение курса валют и запись его в локальную БД, на вход
        # currency - валюта, data_list - список тэгов HTML с их текстом

        data_list = [self.resub(data) for data in data_list]
        with sqlite3.connect('data_base.db') as connection:
            cursor = connection.cursor()
            cursor.execute(SQL_commands.create_table_Currencies_demo)
            i = 0
            for data in data_list:
                if i == 0:
                    date = self.change_date(data)
                elif i == 1:
                    count = int(data)
                elif i == 2:
                    price = re.sub(',', '.', data)
                else:
                    i = 0
                    change = re.sub(',', '.', data)
                    cursor.execute("INSERT INTO Currencies_demo VALUES(?, ?, ?, ?, ?);",
                                   (currency, date, count, price, change))
                    continue
                i += 1

            cursor.executescript(SQL_commands.create_table_Currencies)

    def make_sql_for_countries(self, data_list):  # Чтение списка стран и запись его в локальную БД (data_list -
        # список тэгов HTML с их текстом)

        data_list = [self.resub(data) for data in data_list]
        with sqlite3.connect('data_base.db') as connection:
            cursor = connection.cursor()
            cursor.execute(SQL_commands.create_table_Countries)
            cursor.execute("SELECT COUNT(*) FROM Countries")
            if cursor.fetchone()[0] == 0:  # Запись в БД только если списка стран в ней еще нет
                i = 0
                for data in data_list:
                    if i == 0:
                        country = data
                    elif i == 1:
                        currency = data
                    elif i == 2:
                        code = data
                    else:
                        i = 0
                        number = data
                        cursor.execute("INSERT INTO Countries VALUES(?, ?, ?, ?);", (country, currency, code, number))
                        continue
                    i += 1
