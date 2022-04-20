import pandas as pd
import sqlite3
from patterns.singleton import Singleton


class SqliteHelper(metaclass=Singleton):

    conn = sqlite3.connect("D:/data/temp/utils/ind_stocks.db")

    @staticmethod
    def load_data_from_db(code, start_date, end_date):
        sql = "select * from stocks where code='{}' and valuation_date>='{}' and valuation_date<='{}'".format(
            code, start_date, end_date
        )
        data_frame = pd.read_sql(sql, con=SqliteHelper.conn)
        data_frame = data_frame.set_index("valuation_date")
        data_frame.index = pd.to_datetime(data_frame.index)
        return data_frame


if __name__ == "__main__":
    df = SqliteHelper.load_data_from_db('000001', '2021-01-01', '2022-01-01')
    print(df)
