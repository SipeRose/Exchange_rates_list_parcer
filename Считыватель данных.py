import eel
from currencyreader import CurrencyReader
from relativeupdater import RelativeUpdater
import htmlTablesMaker
import messages


@eel.expose
def get_rates(first_day, first_month, first_year, last_day, last_month, last_year):

    object1 = CurrencyReader()
    object1.data_parser(first_day, first_month, first_year, last_day, last_month, last_year)
    object2 = RelativeUpdater()
    object2.add_date_to_parameters()
    object2.add_to_data_base()

    htmlTablesMaker.maker1()
    messages.show_success1()


@eel.expose
def change_date(new_day, new_month, new_year):

    object3 = RelativeUpdater()
    object3.new_date(new_day, new_month, new_year)

    htmlTablesMaker.maker2()
    messages.show_success2()


eel.init('web')
eel.start('main.html', mode='chrome', size=(400, 670))
