import streamlit as st
import pandas as pd
import sqlite3 as sq
import time
from supplier import download
from style import colors4
def gui():
    drop=st.expander("Items")
    opt=drop.selectbox("",["fetch","Add","Delete"])
    if opt=="fetch":
        try:
            st.dataframe(fetch().style.apply(colors4))
            file_=download(fetch())
            st.download_button(
            "Export",
            file_,
            "items.csv",
            "text/csv",
            key="download-csv"
            )
        except:
            st.warning("Error Encountered")
    elif opt=="Add":
        name=drop.text_input("Item Name")
        date=drop.date_input("creation date")
        category=drop.text_input("Item Category")
        family=drop.text_input("Item Family")
        remark=drop.text_area("remark")
        if drop.button("Add"):
            progress=drop.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            try:
                add(name,date,category,family,remark)
                drop.info("item added successfully")
            except:
                drop.warning("Error Encountered")
    elif opt=="Delete":
        name=drop.text_input("item to delete")
        if drop.button("Delete Item"):
            progress=drop.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            try:
                if list(fetch().name).count(name)>1:
                    delete(name)
                    drop.info("Item deleted successfully")
                else:
                    drop.warning("Item not found..chech name")
            except:
                drop.warning("Error Encountered")
def add(name,date,category,family,remark):
    conn=sq.connect("item.db")
    con=conn.cursor()
    con.execute("create table if not exists prod(name string,created date,category string,family string,remark text)")
    con.execute("insert into prod (name,created,category,family,remark) values(?,?,?,?,?)",(name,date,category,family,remark))
    conn.commit()
def fetch():
    conn=sq.connect("item.db")
    df=pd.read_sql_query("select *from prod",conn)
    return df
def delete(name):
    conn=sq.conect("item.db")
    cur=conn.cursor()
    cur.execute("delete from prod where name=?",(name,))
