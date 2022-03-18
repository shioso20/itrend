import sqlite3 as sq
import pandas as pd
def sr_names():
    conx=sq.connect("organisation.db")
    data=pd.read_sql_query("select *from employees",conx)
    return data.loc[data["post"]=="sales rep"]["name"].to_list()