import streamlit as st
import streamlit_authenticator as stauth
from organ_emp import menu
from style import colors
from PIL import Image
from dist_prod import dist_menu,fetch_info,delete_info
from auth import logs,retrv_log
from organ_emp import fetch_emp
from supplier import incoming,download,dispatch,delete_inc,get_dis,order_menu
from customer import get_customer
import sqlite3
import pandas as pd
from market import visuals
from loc_b import get_loc,add,fetch
import datetime
# created navigation menu using radio button
st.get_option("theme.textColor")
#getting user location
def loc():
    empid=st.text_input("Your Employee id")
    sid=st.text_input("Order serial number")
    date=datetime.datetime.now()
    loc=get_loc()
    if st.button("submit location"):
        #verify employee id
        add(empid,sid,date,loc[0][0],loc[0][1])
        st.info("location added successfully")
st.sidebar.markdown("<i style='text-align: center; font-size: 20px; color: tomato;'>ITREND</i>", unsafe_allow_html=True)
background = Image.open('back.jpeg')
st.sidebar.image(background, width=70)
log_ex=st.sidebar.expander("Create User")
name=log_ex.text_input("Name")
eid=log_ex.text_input("Employee Id")
pwd=log_ex.text_input("Create Password",type="password")
pwd2=log_ex.text_input("Confirm Password",type="password")
#info=fetch_emp()

if log_ex.button("Create User"):
    if pwd!=pwd2:
        st.sidebar.write("password doesn't match")
    elif info[info["empid"]==int(eid)].shape[0]==0:
        st.sidebar.error("Employee id not recognised")
    else:
        logs(name,eid,pwd2)
        st.write("User created successfully")
names,usernames,passwords=retrv_log()
usernames=[str(i) for i in usernames]
passwords = stauth.Hasher(passwords).generate()
logins= stauth.Authenticate(names,usernames,passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)
name,login_status,username = logins.login('Login','sidebar')
if login_status==True:
    rad1 = st.sidebar.radio("menu",["ORGANISATION","DISTRIBUTION MANAGEMENT",
                    "SUPPLY MANAGEMENT","CUSTOMER INFO","MARKET INFO","Delivery Track"])
    if rad1=="ORGANISATION":
        menu()
    elif rad1=="DISTRIBUTION MANAGEMENT":
        dist_menu()
    elif rad1=="SUPPLY MANAGEMENT":
        st.header("Incoming Orders")
        order_menu()
        sel_=st.text_input("barcode")
        if list(get_dis().Barcode).count(sel_)>1:
            st.warning("order already dispatched")
        else:
            if st.button("Dispatch"):
                    if list(fetch_info().Barcode).count(sel_)<1:
                        st.warning("Item not found")
                    else:
                        st.header("Dispatched Orders")
                        st.dataframe(dispatch(fetch_info(),sel_))
                        file_=download(dispatch(fetch_info(),sel_))
                        delete_info(sel_)
                        st.download_button(
                        "Export",
                        file_,
                        "dispatched_orders.csv",
                        "text/csv",
                        key="download-csv"
                        )
    elif rad1=="CUSTOMER INFO":
        st.dataframe(get_customer().style.apply(colors))
        file_=download(get_customer())
        st.download_button(
        "Export",
        file_,
        "customer.csv",
        "text/csv",
        key="download-csv"
        )
    elif rad1=="MARKET INFO":
        data_cat=st.sidebar.selectbox("choose data",["incoming","dispatched"])
        if data_cat=="incoming":
            visuals(incoming())
        elif data_cat=="dispatched":
            conx=sqlite3.connect("dispatch.db")
            data=pd.read_sql_query("select *from dispatch",conx)
            visuals(data)
    elif rad1=="Delivery Track":
        loc_data=fetch()
        st.write(loc_data)
        eid=st.text_input("Employee id")
        serial=st.text_input("Order id")
        if st.button("search"):
            del_loc=loc_data[(loc_data["empid"]==int(eid)) & (loc_data["barcode"]==int(serial))][["latitude","longitude"]]
            st.write(del_loc)
            st.map(del_loc)
elif login_status==False:
    loc()
    st.sidebar.error("incorrect password")
elif login_status==None:
    loc()
    st.sidebar.warning("insert Username and password")
    
