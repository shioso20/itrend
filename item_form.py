import sqlite3 as sq
import pandas as pd
def connect():
    conx=sq.connect("item.db")
    data=pd.read_sql_query("select *from prod",conx)
    return data.name.to_list()