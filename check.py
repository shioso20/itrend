import pandas as pd
import sqlite3
from items import fetch
import requests
import json
from supplier import incoming
from datetime import datetime as dt
df=incoming()
df["date"]=pd.to_datetime(df["date"],format="%Y/%m/%d").dt.date
df["date"]=[str(d) for d in df["date"]]
print(df[(df['date'] >= '2022-02-24') & (df['date'] < '2022-11-02') & (df["eid"]==123)])
