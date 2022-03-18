import sqlite3 as sq
import pandas as pd
def sr_names():
    conx=sq.connect("organisation.db")
    data=pd.read_sql_query("select *from employees",conx)
    return data[["post"]=="sales representatives"].to_list()