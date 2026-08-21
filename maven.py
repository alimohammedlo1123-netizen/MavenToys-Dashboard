import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

st.set_page_config(layout='wide')

BASE_DIR=Path(__file__).parent
data = pd.read_csv(
   BASE_DIR / 'Data.csv'
)
page=st.sidebar.selectbox('Select page',['Home','Analysis'])
if page=='Home':

    st.markdown(
    "<h1 style='text-align: center;'> Maven Store </h1>",
    unsafe_allow_html=True
    )
    st.image(BASE_DIR/"ReITHu0ycQdJQaBCYhl3FtgQOTQ.jpg",use_container_width=True)
    st.title('Sample Of Data')
    st.button('Refresh')
    st.dataframe(data.sample(10))
if page == 'Analysis':
    c1,c2,c3=st.columns([1,1,1],gap='large')
    if 'show_store' not in st.session_state:
        st.session_state.show_store = False
    with c1:
        if st.button('Information Of Store'):
            st.session_state.show_store = True
            st.session_state.show_city=False
            st.session_state.show_location=False
    if 'show_city' not in st.session_state:
        st.session_state.show_city = False
    with c2:
        if st.button('Information Of City'):
            st.session_state.show_city = True
            st.session_state.show_store = False
            st.session_state.show_location=False

    if 'show_location' not in st.session_state:
        st.session_state.show_location = False
    with c3:
        if st.button('Information Of Location'):
            st.session_state.show_location = True
            st.session_state.show_city=False   
            st.session_state.show_store=False
 
    if st.session_state.show_store:
            st.markdown(
    "<h1 style='text-align: center;'> Information Of Store </h1>",
    unsafe_allow_html=True
    )
            Store = st.selectbox(
                'Select',
                data['Store_Name'].value_counts().index
            )

            temp = data[data['Store_Name'] == Store]

            c1, c2, c3, c4 = st.columns([1,1,1,1], gap='large')

            with c1:
                st.metric(
                    f':city_sunset: Store In City',
                    temp['Store_City'].iloc[0]
                )
            with c2:
                st.metric(f':round_pushpin: Store In Location',
                    temp['Store_Location'].iloc[0])    
            with c3:
                st.metric(f':clock10: Store Open In Date',
                    temp['Store_Open_Date'].iloc[0])
            with c4:
                st.metric(f':dollar: Store Revenue',
                    temp['Revenue'].sum())    

            sales = data['Store_Name'].value_counts()

            colors = [
            'red' if store == Store else 'gray'
            for store in sales.index
            ]
            group=data.groupby(['Store_Name'])['Revenue'].sum()
            fig=px.line(x=group.index,y=group.values,title='Store_Name VS Revenue',height=1000,width=1000)
            fig.update_yaxes(title='Revenue')
            st.plotly_chart(fig)

            fig = px.bar(x=sales.index, y=sales.values,title='Sales Of Each Store')
            fig.update_yaxes(title='Sales')
            fig.update_traces(marker_color=colors)
            st.plotly_chart(fig)    
            col1, col2 = st.columns(2)
            sales = data["Store_Name"].value_counts()

            with col1:
                st.metric(
                "🏆 Top Store",
                sales.index[0],
                f"{sales.iloc[0]} Sales"
            )

            with col2:
                st.metric(
                "📉 Lowest Store",
                sales.index[-1],
                f"{sales.iloc[-1]} Sales"
            )
    
    if st.session_state.show_city:
        st.markdown(
            "<h1 style='text-align: center;'> Information Of City </h1>",
            unsafe_allow_html=True)
        City=st.selectbox('Select',data['Store_City'].value_counts().index)
        c1,c2=st.columns([1,1],gap='large')
        temp = data[data['Store_City'] == City]
        with c1:
            st.metric(':round_pushpin: City in Location',temp['Store_Location'].iloc[0])
        with c2:
            st.metric(':dollar: City Revenue',temp['Revenue'].sum())
        groupby=data.groupby(['Store_City'])['Revenue'].sum()
        fig=px.line(x=groupby.index,y=groupby.values,title='Store City Of Revnue')
        fig.update_yaxes(title="Revnue")
        st.plotly_chart(fig)
        groupby=data.groupby(['Store_City'])['Store_Name'].nunique()
        fig=px.bar(x=groupby.index,y=groupby.values,title='Number Of Stores in Each City')
        fig.update_yaxes(title="Number Of Stores")
        st.plotly_chart(fig)        
        fig=px.bar(x=data['Store_City'].value_counts().index,y=data['Store_City'].value_counts().values,title='Store City Sales',height=750,width=1000)
        fig.update_yaxes(title='Sales')
        st.plotly_chart(fig)
    if st.session_state.show_location:
        st.markdown(
            "<h1 style='text-align: center;'> Information Of Location </h1>",
            unsafe_allow_html=True)
        Location=st.selectbox('Select',data['Store_Location'].value_counts().index)
        temp=data[data['Store_Location']==Location]
        c1,c2,c3=st.columns([7,10,1],gap='large')
        with c2:
            st.metric(':dollar: Location Revenue',temp['Revenue'].sum())
        group5=data.groupby(['Store_Location'])['Revenue'].sum()
        fig=px.line(x=group5.index,y=group5.values,title='Store_Location VS Revenue',height=1000,width=1000)
        fig.update_yaxes(title='Revenue')
        st.plotly_chart(fig)
        group3=data.groupby(['Store_Location'])['Store_City'].nunique()
        fig=px.bar(x=group3.index,y=group3.values,height=500,width=750,title='Numer of city in each Location')
        fig.update_yaxes(title='Number of City')
        st.plotly_chart(fig)
        group4=data.groupby(['Store_Location'])['Store_Name'].nunique()
        fig=px.bar(x=group4.index,y=group4.values,height=500,width=750,title='Number of stores in each Location')
        fig.update_yaxes(title='Number of Stores')
        st.plotly_chart(fig)
        fig=px.bar(x=data['Store_Location'].value_counts().index,y=data['Store_Location'].value_counts().values,title='Store_Location Sales',height=750,width=750)
        fig.update_yaxes(title='Sales')
        st.plotly_chart(fig)