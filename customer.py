import sqlite3
import pandas
def get_customer():
    conx=sqlite3.connect("order.db")
    data=pandas.read_sql_query("select *from orders",conx)
    sel_col=["customer","cphone","town","loc","ddate"]
    return data[sel_col]
