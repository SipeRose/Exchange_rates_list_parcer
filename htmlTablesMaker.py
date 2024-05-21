import pandas as pd
import sqlite3

# для вывода таблиц Pandas, содержащих данные из локальных БД, в формате HTML


def maker1():

    with sqlite3.connect('data_base.db') as connection:
        df1 = pd.read_sql("select * from Currencies order by Valuta, Date", connection)
        df1 = df1.rename(columns={'Valuta': 'Валюта', 'Date': 'Дата', 'Count': 'Количество', 'Price': 'Цена',
                                  'Change': 'Изменение'})
        df2 = pd.read_sql("select * from Countries order by Country", connection)
        df2 = df2.rename(columns={'Country': 'Страна', 'Currency': 'Валюта', 'Code': 'Код', 'Number': 'Номер'})
        df3 = pd.read_sql("select * from Relative_change order by Valuta, Date", connection)
        df3 = df3.rename(columns={'Valuta': 'Валюта', 'Date': 'Дата',
                                  'Price_Relative_Change_in_percents': 'Относительное изменение цены, %'})
        df4 = pd.read_sql("select * from Parameters_table", connection)
        df4 = df4.rename(columns={'Day': 'Дата'})

    pd.set_option('display.max_rows', None)
    df1.to_html('Курсы валют.html')
    df2.to_html('Список валют.html')
    df3.to_html('Относительные изменения курса.html')
    df4.to_html('Таблица параметров.html')


def maker2():

    with sqlite3.connect('data_base.db') as connection:
        df1 = pd.read_sql("select * from Currencies order by Valuta, Date", connection)
        df1 = df1.rename(columns={'Valuta': 'Валюта', 'Date': 'Дата', 'Count': 'Количество', 'Price': 'Цена',
                                  'Change': 'Изменение'})
        df2 = pd.read_sql("select * from Relative_change order by Valuta, Date", connection)
        df2 = df2.rename(columns={'Valuta': 'Валюта', 'Date': 'Дата',
                                  'Price_Relative_Change_in_percents': 'Относительное изменение цены, %'})
        df3 = pd.read_sql("select * from Parameters_table", connection)
        df3 = df3.rename(columns={'Day': 'Дата'})

    pd.set_option('display.max_rows', None)
    df1.to_html('Курсы валют.html')
    df2.to_html('Относительные изменения курса.html')
    df3.to_html('Таблица параметров.html')
