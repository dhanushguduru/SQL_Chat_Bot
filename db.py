import sqlite3
import pandas as pd

class CreateDataBase:

    @staticmethod
    def loadExcel(filename, table_name, db_name):
        connection = sqlite3.connect(db_name)
        df = pd.read_excel(filename)
        df.to_sql(name = table_name, con = connection, if_exists="replace", index=True)
        connection.commit()
        connection.close()

    @staticmethod
    def loadCsv(filename, table_name, db_name):
        connection = sqlite3.connect(db_name)
        df = pd.read_csv(filename)
        df.to_sql(name = table_name, con = connection, if_exists="replace", index=True)
        connection.commit()
        connection.close()