create_table_Currencies_demo = """
CREATE TABLE IF NOT EXISTS Currencies_demo(
Valuta VARCHAR(30),
Date DATE,
Count INT,
Price NUMERIC(8,4),
Change NUMERIC(7,4)
);
"""

create_table_Currencies = """
    CREATE TABLE IF NOT EXISTS Currencies(
    Valuta VARCHAR(30),
    Date DATE,
    Count INT,
    Price NUMERIC(8,4),
    Change NUMERIC(7,4)
    );
    INSERT INTO Currencies (Valuta, Date, Count, Price, Change)
    SELECT Valuta, Date, Count, Price, Change
    FROM Currencies_demo
    WHERE (Valuta, Date, Count, Price, Change) NOT IN (SELECT Valuta, Date, Count, Price, Change FROM Currencies);
    DROP TABLE Currencies_demo;
    """

create_table_Countries = """
        CREATE TABLE IF NOT EXISTS Countries(
        Country VARCHAR(40),
        Currency VARCHAR(40),
        Code VARCHAR(3),
        Number VARCHAR(3)
        );
        """

create_table_Parameters_table = """
    DROP TABLE IF EXISTS Parameters_table;
    CREATE TABLE Parameters_table(
    Day TEXT
    );
    """

create_ordered_table_Currencies = '''
CREATE TABLE orderedCurrencies(
Valuta VARCHAR(30),
Date DATE,
Count INT,
Price NUMERIC(8,4),
Change NUMERIC(7,4)
);
INSERT INTO orderedCurrencies (Valuta, Date, Count, Price, Change)
SELECT Valuta, Date, Count, Price, Change
FROM Currencies ORDER BY Valuta, Date;
DROP TABLE Currencies;
ALTER TABLE 'orderedCurrencies' RENAME TO 'Currencies'
'''

create_table_Relative_change = """
    CREATE TABLE IF NOT EXISTS Relative_change(
    Valuta VARCHAR(30),
    Date DATE,
    Price_Relative_Change_in_percents NUMERIC(6,4)
    );
    """

insert_into_table_Relative_change = """
    INSERT INTO Relative_change (Valuta, Date, Price_Relative_Change_in_percents)
    SELECT Valuta, Date, printf("%.5f", ((Price/?)-1)*100) AS Price_Relative_Change_in_percents
    FROM Currencies
    WHERE (Valuta, Date) NOT IN (SELECT Valuta, Date FROM Relative_change) AND  Valuta = ?;
    """