from enum import unique
from fetch_lock_data import fetch_lock_delay, fetch_traffic_report, fetch_lock_queue_data, xml_to_dataframe, json_to_dataframe, fetch_stall_stoppage, fetch_tonnage_report, fetch_lock_status_report
import streamlit as st
import pandas as pd 
st.set_page_config(layout="wide")



st.title('Water Locks Data')



col1, col2 = st.columns([1,4])

locks_of_interest = { "Port Allen":"01" , "Bayou Sorrel":"02", "Leland Bowman":"77", "Calcasieu":"08"}

with col1: 

    river_code = st.selectbox('Choose river:', ["GI"])
    lock_name =  st.selectbox('Choose locks:', list(locks_of_interest.keys())) 
    in_month_year = st.text_input("Enter date:", "092023")
    lock_no = locks_of_interest[lock_name]
with col2:
    st.header('Lock Queue Data')
    data = fetch_lock_queue_data(river_code, lock_no)
    df = xml_to_dataframe(data)
    st.write(df)

    # st.header('Stoppage Data for dates')
    # stoppage_data = fetch_stall_stoppage("22082023", "22092023")
    # st.write(stoppage_data)

    # df = json_to_dataframe(stoppage_data)
    # st.write(df.head())

    st.header('Traffic Report')
    traffic_report = fetch_traffic_report(river_code, lock_no)
    st.write(traffic_report)
    traffic_df = json_to_dataframe(traffic_report)
    st.write(traffic_df)


    st.header('Tonnage Reports')
    tonnage_report = fetch_tonnage_report(river_code, lock_no, in_month_year)
    # st.write(tonnage_report)

    tonnage_df = json_to_dataframe(tonnage_report)
    st.write(tonnage_df)


    st.header('River Lock Status Report')
    lock_report = fetch_lock_status_report(river_code)
    lock_report_df = json_to_dataframe(lock_report)
    st.write(lock_report_df)

    

    st.header('Any Lock Delays')
    lock_delay = fetch_lock_delay()
    lock_delay_df = json_to_dataframe(lock_delay)
    st.write(lock_delay_df)


    st.header('Stoppage')
    # st.header('Stoppage Data for dates')
    beg_date = st.text_input('Stoppage Start Date:', "22082023")
    end_date = st.text_input('Stoppage End Date:', "22082023")

    stoppage_data = fetch_stall_stoppage(beg_date, end_date)
    # stoppage_data = fetch_stall_stoppage()
    # st.write(stoppage_data)
    stoppage_df = json_to_dataframe(stoppage_data)
    st.write(stoppage_df)


    st.header('Delivered Ships')

    boats = pd.read_excel('data/BECHTEL HAUL BARGE.xlsx', skiprows= 2)
    boats =boats.dropna(subset=[boats.columns[0]]).dropna(axis=1)

    unique_boats = list(set(boats['Tug Boat']))

    unique_boats = [boat.upper()+' (TOW)' for boat in unique_boats]
    # st.write(unique_boats)
    boats_in_lock = [boat for boat in unique_boats if boat in traffic_df['vesselName'].tolist()]
    report_on_boat = traffic_df.set_index('vesselName').loc[boats_in_lock]
    st.write(report_on_boat)
    # boats['Tug Boat']
    # .dropna(subset=['Tow No. ])

    # boats.columns = boats.columns
    # st.write(boats[[ boats.columns[0], 'Tons']])
    st.write(boats)

    # st.write(set(boats['Tug Boat'].dropna(subset=['Tow No.'])))

