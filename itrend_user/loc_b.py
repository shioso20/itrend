import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import datetime
import sqlite3 as sq
import pandas as pd
empid=st.text_input("Your Employee id")
sid=st.text_input("Order serial number")
date=datetime.datetime.now()
loc_button = Button(label="Get Location")
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition(
        (loc) => {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    """))
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)
loc=[]
if result:
    if "GET_LOCATION" in result:
        locs=result.get("GET_LOCATION")
        loc.append([*locs.values()])

def add(empid,sid,date,lat,log):
    conn=sq.connect("loc.db")
    con=conn.cursor()
    con.execute("create table if not exists location(name string,barcode string,delivered date,latitude float,longitude float)")
    con.execute("insert into location (name,barcode,delivered,latitude,longitude) values(?,?,?,?,?)",(empid,sid,date,lat,log))
    conn.commit()
def fetch():
    conn=sq.connect("loc.db")
    df=pd.read_sql_query("select *from location",conn)
    return df
if st.button("submit"):
    add(empid,sid,date,loc[0][0],loc[0][1])
    df=fetch()
    st.map(df[df["name"]==123][["latitude","longitude"]])