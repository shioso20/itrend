import sqlite3 as sq
import pandas as pd
#populate users credentials created by admin
def con_both():
    con1=sq.connect("logs.db")
    con2=sq.connect("order.db")
    cu2=con2.cursor()
    df=pd.read_sql_query("select *from log",con1)
    for i in df.empid.to_list():
        for j in df.password.to_list():
            cu2.execute("insert into member (eid,password) values(?,?)",(i,j))
    con2.commit()
