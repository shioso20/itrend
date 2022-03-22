import streamlit as st
import sqlite3
import pandas as pd
import time
from supplier import download
from style import colors4
def menu2(col1,col3):
    exp=col3.expander("Supply field")
    radc2=exp.selectbox("",["fetch","add","edit","delete"])
    if radc2=="add":
        # add product info
        shop=exp.text_input("Shop name")
        category=exp.text_input("Shop Category")
        supplier=exp.text_input("Supplier/Manager Name")
        supplier_no=exp.text_input("Supplier Phone No")
        Region=exp.text_input("Region")
        Town=exp.text_input("Town")
        street=exp.text_input("street")
        remark=exp.text_area("Remark")
        if exp.button("add shop"):
            progress=exp.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            try:
                add_prod(shop,category,supplier,supplier_no,Region,Town,street,remark)
                exp.info("shop Added successfully")
            except:
                st.error("Encountered some error")
    elif radc2=="fetch":
        # input search by product id
        s_fetch_r=exp.radio("",["All","filter_by"])
        if s_fetch_r=="filter_by":
            search=exp.text_input("search by shop id")
            if exp.button("filter shop"):
                exp.write("searching product")
                progress=exp.progress(0)
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
                    st.error("Encountered some error")
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
                st.error("Encountered some error")


    elif radc2=="edit":
        # input edit by product id
        p_id=exp.text_input("edit by product id")
        change=exp.selectbox("field to edit",["Supplier","Category","Family","shopname"])
        sets=exp.text_input("new value")
        if exp.button("edit shop"):
            progress=exp.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            data=fetch_prod()
            d_f=data[data["sid"]==int(p_id)]
            try:
                if d_f.shape[0]>0:
                    edit_prod(change,sets,p_id)
                    exp.info("Edited successfully")
                else:
                    exp.warning("shop not found")
            except:
                st.error("Encountered some error")
    elif radc2=="delete":
        p_id=exp.text_input("shop id to delete")
        if exp.button("delete shop"):
            progress=exp.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            data=fetch_prod()
            d_f=data[data["sid"]==int(p_id)]
            try:
                if d_f.shape[0]>0:
                    delete_prod(p_id)
                    exp.info("shop removed successfully")
                else:
                    exp.warning("shop not found")
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
