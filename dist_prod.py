import streamlit as st
import sqlite3
import pandas as pd
import time
from organ_sup import fetch_prod
from items import fetch
from supplier import download
from style import colors5
def dist_menu():
        pander=st.expander("Add stock")
        Barcode=pander.text_input("Scan Barcode")
        Item_name=pander.selectbox("Item name",fetch()["name"].tolist())
        Item_colour=pander.text_input("Item colour")
        Item_Desc=pander.text_input("Item description")
        Item_size=pander.text_input("Item size")
        Item_material=pander.text_input("Item_material")
        Buying_price=pander.text_input("Buying Price")
        Category=pander.selectbox("Category",fetch()["category"].tolist())
        Family=pander.selectbox("Family",fetch()["family"].tolist())
        sub_family=pander.selectbox("Sub Family",fetch()["category"].tolist())
        Brand_name=pander.text_input("Brand_name")
        supplier=pander.selectbox("Supplier Name",fetch_prod()["supplier"].tolist())
        supplier_NO=pander.text_input("Supplier Phone Number")
        shop=pander.selectbox("Shop Name",fetch_prod()["shop"].tolist())
        if pander.button("Confirm"):
            p=st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                p.progress(i+1)
            add_info(Barcode,Item_name,Item_colour,Item_Desc,Item_size,Item_material,Buying_price,Category,Family,sub_family,Brand_name,supplier,supplier_NO,shop)
            if True:
                st.info("Item added successfully")
            else:
                st.error("Error Encountered")
        c1,c2=st.columns((1,1))
        fetch_r=c1.radio("",["All","filter"])
        if fetch_r=="filter":
            id=c1.text_input("Fetch by pid")
            if c1.button("fetch"):
                data=fetch_info()
                f_data=data[data["pid"]==int(id)]
                st.write("--fetching")
                try:
                    st.dataframe(f_data.style.apply(colors5))
                    file_=download(f_data)
                    st.download_button(
                    "Export",
                    file_,
                    "filtered_stock.csv",
                    "text/csv",
                    key="download-csv"
                    )
                except:
                    st.error("Error Encountered")
        elif fetch_r=="All":
            try:
                st.dataframe(fetch_info().style.apply(colors5))
                file_=download(fetch_info())
                st.download_button(
                "Export",
                file_,
                "all_stock.csv",
                "text/csv",
                key="download-csv"
                )
            except:
                st.error("Error Encountered")
        d_id = c2.text_input("Delete by barcode")
        if c2.button("Delete"):
            delete_info(d_id)
            if True:
                st.info("Item Deleted successfully")
            else:
                st.error("Error Encountered")

def add_info(Barcode,Item_name,Item_colour,Item_Desc,Item_size,Item_material,Buying_price,Category,Family,sub_family,Brand_name,supplier,supplier_NO,shop):
    # adding distribution data
    conn=sqlite3.connect("stock.db")
    con=conn.cursor()
    con.execute("create table if not exists dist_prod(pid integer primary key autoincrement,Barcode,Item_name string,Item_colour string,Item_Desc text,Item_size string,Item_material string,Buying_price float,Category string,Family string,sub_family string,Brand_name string,supplier string,supplier_NO string,shop string)")
    con.execute("insert into dist_prod (Barcode,Item_name,Item_colour,Item_Desc,Item_size,Item_material,Buying_price,Category,Family,sub_family,Brand_name,supplier,supplier_NO,shop) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(Barcode,Item_name,Item_colour,Item_Desc,Item_size,Item_material,Buying_price,Category,Family,sub_family,Brand_name,supplier,supplier_NO,shop,))
    conn.commit()

def fetch_info():
    # extract distribution data
    conn=sqlite3.connect("stock.db")
    data = pd.read_sql_query("select *from dist_prod",conn)
    return data


def delete_info(barcode):
    # delete distribution info by id
    conn=sqlite3.connect("stock.db")
    con=conn.cursor()
    con.execute("delete from dist_prod where Barcode=?",(barcode,))
    conn.commit()


