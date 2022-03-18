import seaborn as sn
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
#creating visualisations of orders
def visuals(data):
    col1=st.sidebar
    col2,col3=st.columns((1,1))
    row=col1.selectbox("bar plot x-axis",data.columns)
    time_plot(data,"date","quant")
    try:
        bar(data,row,"quant")
    except:
        st.warning("select appropriate field")
def bar(data,row,col):
    fig=plt.figure(figsize=(8,3))
    sn.barplot(x=row,y=col,data=data,estimator=sum)
    st.pyplot(fig)
def time_plot(df,x,y):
    fig = px.line(df, x=x, y=y, title='sales over time')
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)
