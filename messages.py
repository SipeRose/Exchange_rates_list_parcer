from tkinter.messagebox import showinfo
import tkinter


def show_success1():
    root = tkinter.Tk()
    root.withdraw()
    showinfo(title='Успешно', message='Информация добавлена в файлы Курсы валют.html, Список валют.html,'
                                      ' Относительные изменения курса.html, Таблица параметров.html и '
                                      'в базу данных data_base.db')
    root.update()


def show_success2():
    root = tkinter.Tk()
    root.withdraw()
    showinfo(title='Успешно', message='Информация обновлена в файлах Относительные изменения курса.html, '
                                      'Таблица параметров.html и в базе данных data_base.db')
    root.update()
