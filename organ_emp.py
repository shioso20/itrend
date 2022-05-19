import streamlit as st
import pandas as pd
import sqlite3
import time
from PIL import Image
from organ_sup import menu2
import datetime
from items import gui
from style import colors3,colors4
from supplier import download
#import random
def menu():
    gui()
    col1,col3=st.columns((1,1))
    # create selection menu
    col1.header("Employee field")
    radc1 = col1.radio("options",["fetch","add","edit","delete"])

    # saving employee infos
    if radc1=="add":
        empid=col1.text_input("Employee ID ",placeholder="YYMMDDN0")
        id_no=col1.text_input("National id Number")
        name=col1.text_input("full name")
        gender=col1.selectbox("Gender",["Male","Female",""])
        birth=col1.date_input("Date of birth",min_value=datetime.date(year=1960,month=1,day=1))
        doj=col1.date_input("date of joining",min_value=datetime.date(year=1960,month=1,day=1))
        resign=col1.date_input("date of resigning",min_value=datetime.date(year=1960,month=1,day=1))
        comp=col1.text_input("company")
        Dep=col1.text_input("Department")
        post=col1.text_input("Post Title")
        role=col1.text_input("Role name")
        status=col1.selectbox("Status",["working","leave","Resigned"])
        attr=col1.text_input("Job attributes")
        bank=col1.text_input("Bank name")
        bank_no=col1.text_input("Bank Card Number")
        Nation=col1.text_input("Nationality")
        addr=col1.text_input("Address")
        Emerg=col1.text_input("Emergency contact number")
        marital=col1.selectbox("Marital status",["Married","Single",""])
        edu=col1.selectbox("Education Level",["Primary school","High school","Bachelors","Masters"])
        major=col1.text_input("Major")
        gradu=col1.date_input("Graduation date",min_value=datetime.date(year=1960,month=1,day=1))
        salary=col1.text_input("Salary")
        remark=col1.text_area("comments")
        if col1.button("ADD INFO"):
            p=col1.progress(0)
            for i in range(100):
                time.sleep(0.01)
                p.progress(i+1)
            try:
                add_emp(empid,id_no,name,gender,birth,doj,resign,comp,
                Dep,post,role,status,attr,bank,bank_no,Nation,
                addr,Emerg,marital,edu,major,gradu,salary,remark)
                col1.info("Details added successfully")
            except:
                st.error("Encountered some error")


    # search employee by id
    elif radc1=="fetch":
        # input search by employee id
        emp_rad=col1.radio("",["All","filter"])
        if emp_rad=="All":
  
                col1.dataframe(fetch_emp().style.apply(colors4))
                file_=download(fetch_emp())
                col1.download_button(
                "Export Employees",
                file_,
                "all_employees.csv",
                "text/csv",
                key="download-csv"
                )
            
        elif emp_rad=="filter":
            search=col1.text_input("search by id")
            if col1.button("fetch"):
                p=col1.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    p.progress(i+1)
                try:
                    data=fetch_emp()
                    d_f=data[data["empid"]==int(search)]
                    col1.dataframe(d_f)
                    file_=download(d_f)
                    col1.download_button(
                    "Export Employees",
                    file_,
                    "employees.csv",
                    "text/csv",
                    key="download-csv"
                    )
                except:
                    st.error("Encountered some error")
    elif radc1=="edit":
        # input for id to edit
        edit_id=col1.text_input("edit employee id")
        change=col1.selectbox("field to edit",["idno","name","gender","DOB","DOJ","DOS"
        ,"company","Department","post","role","status","job_attribute","Bank","bank_no",
        "nationality","address","emergency_no","marital_status","education","major","DOG","salary","remark"])
        sets=col1.text_input("new value")
        if col1.button("edit"):
            p=col1.progress(0)
            for i in range(100):
                time.sleep(0.01)
                p.progress(i+1)
            data=fetch_emp()
            d_f=data[data["empid"]==int(edit_id)]
            try:
                if d_f.shape[0]>0:
                    edit_emp(change,sets,edit_id)
                    col1.info("Edited successfully")
                else:
                    col1.warning("Employee not found..check id")
            except:
                col1.error("Encountered some error")

    elif radc1=="delete":
        emp_id=col1.text_input("employee id to delete")
        if col1.button("Delete"):
            p=col1.progress(0)
            for i in range(100):
                time.sleep(0.01)
                p.progress(i+1)
            data=fetch_emp()
            d_f=data[data["empid"]==int(emp_id)]
            try:
                if d_f.shape[0]>0:
                    delete_emp(emp_id)
                    col1.info("Employee removed successfully")
                else:
                    col1.warning("Employee  not found..check id")

            except:
                col1.error("Encountered some error")
    menu2(col1,col3)



def add_emp(empid,id_no,name,gender,birth,doj,resign,comp,
Dep,post,role,status,attr,bank,bank_no,Nation,
addr,Emerg,marital,edu,major,gradu,salary,remark):
    # sqlite add employee info code here
    conn=sqlite3.connect("organisation.db")
    con=conn.cursor()
    con.execute("create table if not exists employees(empid integer,idno integer,name text,gender string,DOB date,DOJ date,DOS date,company string,Department string,post string,role string,status string,job_attribute string,bank string,bank_no string,nationality string,address string,emergency_no string,marital_status string,education string,major string,DOG date,salary float,remark text)")
    con.execute("insert into employees (empid,idno,name,gender,DOB,DOJ,DOS,company,Department,post,role,status,job_attribute,Bank,bank_no,nationality,address,emergency_no,marital_status,education,major,DOG,salary,remark) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(empid,id_no,name,gender,birth,doj,resign,comp,Dep,post,role,status,attr,bank,bank_no,Nation,addr,Emerg,marital,edu,major,gradu,salary,remark,))
    conn.commit()

def fetch_emp():
    # sqlite fetch code here
    conn=sqlite3.connect("organisation.db")
    data=pd.read_sql_query("select *from employees",conn)

    return data

def edit_emp(val,set,id):
    # sqlite edit code
    conn=sqlite3.connect("organisation.db")
    con=conn.cursor()
    cmd="update employees set "+str(val)+" =? "+"where empid=?"
    con.execute(cmd,(set,id,))
    conn.commit()

def delete_emp(id):
     # delete employee by id.
     conn=sqlite3.connect("organisation.db")
     con=conn.cursor()
     con.execute("delete from employees where empid=?",(id,))
     conn.commit()
