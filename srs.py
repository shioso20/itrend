import sqlite3 as sq
import pandas as pd
def sr_names():
    conx=sq.connect("organisation.db")
    data=pd.read_sql_query("select *from employees",conx)
    return data.loc[data["post"]=="sales rep"]["name"].to_list()
def get_emp_id(id):
    connx=sq.connect("organisation.db")
    emp_data=pd.read_sql_query("select *from employees",connx)
    x=[]
    if len(emp_data.loc[emp_data["empid"]==id]["name"].to_list())>0:
        x.append(emp_data.loc[emp_data["empid"]==id]["name"].to_list()[0])
    else:
        x.append("")
    return x[0]
