import streamlit as st
import sqlite3
import pandas as pd
import time
from supplier import download
from style import colors4
def menu2(col1,col3):
    col3.header("Supply field")
    radc2=col3.radio("",["fetch","add","edit","delete"])
    if radc2=="add":
        # add product info
        shop=col3.text_input("Shop name")
        category=col3.text_input("Shop Category")
        supplier=col3.text_input("Supplier/Manager Name")
        supplier_no=col3.text_input("Supplier Phone No")
        Region=col3.text_input("Region")
        Town=col3.text_input("Town")
        street=col3.text_input("street")
        remark=col3.text_area("Remark")
        if col3.button("add shop"):
            progress=col3.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            try:
                add_prod(shop,category,supplier,supplier_no,Region,Town,street,remark)
                col3.info("shop Added successfully")
            except:
                st.error("Encountered some error")
    elif radc2=="fetch":
        # input search by product id
        s_fetch_r=col3.radio("",["All","filter_by"])
        if s_fetch_r=="filter_by":
            search=col3.text_input("search by shop id")
            if col3.button("filter shop"):
                col3.write("searching product")
                progress=col3.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i+1)
                try:
                    s_fetch_d=fetch_prod()
                    s_f_fetch_d=s_fetch_d[s_fetch_d["sid"]==int(search)]
                    col3.dataframe(s_f_fetch_d.style.apply(colors4))
                    file_=download(s_f_fetch_d)
                    col3.download_button(
                    "Export",
                    file_,
                    "filtered_shops.csv",
                    "text/csv",
                    key="download-csv"
                    )
                except:
                    st.error("")
        elif s_fetch_r=="All":
            try:
                col3.dataframe(fetch_prod().style.apply(colors4))
                file_=download(fetch_prod())
                col3.download_button(
                "Export",
                file_,
                "all_shops.csv",
                "text/csv",
                key="download-csv"
                )
            except:
                st.info("")


    elif radc2=="edit":
        # input edit by product id
        p_id=col3.text_input("edit by product id")
        change=col3.selectbox("field to edit",["Supplier","Category","Family","shopname"])
        sets=col3.text_input("new value")
        if col3.button("edit shop"):
            progress=col3.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            data=fetch_prod()
            d_f=data[data["sid"]==int(p_id)]
            try:
                if d_f.shape[0]>0:
                    edit_prod(change,sets,p_id)
                    col3.info("Edited successfully")
                else:
                    col3.warning("shop not found")
            except:
                st.error("Encountered some error")
    elif radc2=="delete":
        p_id=col3.text_input("shop id to delete")
        if col3.button("delete shop"):
            progress=col3.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            data=fetch_prod()
            d_f=data[data["sid"]==int(p_id)]
            try:
                if d_f.shape[0]>0:
                    delete_prod(p_id)
                    col3.info("shop removed successfully")
                else:
                    col3.warning("shop not found")
            except:
                st.error("Encountered some error")
def add_prod(shop,category,supplier,supplier_no,Region,Town,street,remark):
    # sqlite add employee info code here
    conn=sqlite3.connect("shops.db")
    con=conn.cursor()
    con.execute("create table if not exists supply(sid integer primary key autoincrement,shop string,Category string,supplier string,supplier_no string,Region string,Town string,street string,Remark text)")
    con.execute("insert into supply (shop,Category,supplier,supplier_no,Region,Town,street,Remark) values (?,?,?,?,?,?,?,?)",(shop,category,supplier,supplier_no,Region,Town,street,remark,))
    conn.commit()


def fetch_prod():
    # sqlite fetch code here
    conn=sqlite3.connect("shops.db")
    data=pd.read_sql_query("select *from supply",conn)


    return data

def edit_prod(val,set,id):
    # sqlite edit code
    conn=sqlite3.connect("shops.db")
    con=conn.cursor()
    cmd="update supply set "+str(val)+" =? "+"where sid=?"
    con.execute(cmd,(set,id,))
    conn.commit()

def delete_prod(id):
     # delete products by id.
     conn=sqlite3.connect("shops.db")
     con=conn.cursor()
     con.execute("delete from supply where sid=?",(id,))
     conn.commit()
