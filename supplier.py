import sqlite3 as sq
import pandas as pd
import requests
import json
import streamlit as st
from style import colors
import numpy as np
# fetch orders made
def order_menu():
    df=incoming()
    c1=st.sidebar
    c1.write("filter orders")
    empid=c1.text_input("Emp Id")
    c1.write(empid)
    date1=c1.date_input("From")
    date1=date1.strftime("%Y-%m-%d")
    c1.write(date1)
    date2=c1.date_input("To")
    date2=date2.strftime("%Y-%m-%d")
    if c1.button("filter"):
        if empid=="":
            try:
                st.dataframe(filter_date(df,date1,date2).style.apply(colors))
                file_=download(filter_date(df,date1,date2))
                st.download_button(
                "Export",
                file_,
                "filtered_orders.csv",
                "text/csv",
                key="download-csv"
                )
            except Exception as e:
                st.error("Error Encountered")
        elif empid!="":
            try:
                st.dataframe(filter_all(df,date1,date2,empid).style.apply(colors))
                file_=download(filter_all(df,date1,date2,empid))
                st.download_button(
                "Export",
                file_,
                "filtered_orders.csv",
                "text/csv",
                key="download-csv"
                )
            except Exception as e:
                st.error("Error Encountered")
        else:
            try:
                st.dataframe(df)
                file_=download(filter_date(df))
                st.download_button(
                "Export",
                file_,
                "all_orders.csv",
                "text/csv",
                key="download-csv"
                )
            except:
                st.error("Error Encountered")





def incoming():
    try:
        data=pd.read_html("http://itrend.pythonanywhere.com/incoming")
        data=data[0]
        data["date"]=pd.to_datetime(data["date"],format="%Y/%m/%d").dt.date
        data["date"]=[str(d) for d in data["date"]]
        return data
    except:
        st.error("Server Error...Contact Server Admin")

def download(data):
    return data.to_csv().encode('utf-8')
def dispatch(data,barcode):
    sel_data=data.loc[data["Barcode"]==barcode]
    con=sq.connect("dispatch.db")
    sel_data.to_sql(name="dispatch",con=con,if_exists="append")
    con2=sq.connect("dispatch.db")
    sel_data=pd.read_sql_query('select *from dispatch',con2)
    # delete from incoming
    return sel_data
def get_dis():
    conx=sq.connect("dispatch.db")
    dis_dat=pd.read_sql_query("select *from dispatch",conx)
    return dis_dat
def delete_inc(id):
    conn=sq.connect("dispatch.db")
    con=conn.cursor()
    con.execute("delete from dispatch where id=?",(id,))
    conn.commit()
def filter_date(df,fr,to):
    return df[(df['date'] >= str(fr)) & (df['date'] <= str(to))]
def filter_all(df,fr,to,eid):
    return df[(df['date'] >= str(fr)) & (df['date'] <= str(to)) & (df["eid"]==int(eid))]
def filter_eid(df,eid):
    return df[df["eid"]==int(eid)]
def compare(df1,df2):
    x=list(df2.barcode)
    df1["status"]=np.where((df1["Barcode"]==i for i in x),"Waiting","Delivered")
    return df1
