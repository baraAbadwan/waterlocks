import requests
import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as st
import requests

@st.cache_data
def fetch_lock_queue_data(river_code, lock_no):
    base_url = "https://ndc.ops.usace.army.mil/ords/lockqueue_xml"
    params = {
        'in_river': river_code,
        'in_lock': lock_no
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to fetch data. HTTP Status Code: {response.status_code}"


@st.cache_data
def xml_to_dataframe(xml_data):
    root = ET.fromstring(xml_data)
    
    all_data = []
    
    # Assuming each child of the root represents a row of data
    for child in root:
        data = {}
        for element in child:
            data[element.tag] = element.text
        all_data.append(data)
    
    return pd.DataFrame(all_data)



def json_to_dataframe(json_data):
    return pd.DataFrame(json_data)
# Example usage:
# river_code = "GI"
# lock_no = "01"
# data = fetch_lock_queue_data(river_code, lock_no)
# print(data)


@st.cache_data
def fetch_stall_stoppage(begin_date=None, end_date=None):
    base_url = f"https://ndc.ops.usace.army.mil/ords/lpms/stall_stoppage_json"
    params = {}
    if begin_date and end_date:
        base_url = f"https://ndc.ops.usace.army.mil/ords/lpms/stall_stoppage_json?begin_date={begin_date}&end_date={end_date}"

        params['begin_date'] = begin_date
        params['end_date'] = end_date

    
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to fetch data. HTTP Status Code: {response.status_code}"

@st.cache_data
def fetch_lock_delay():
    base_url = "https://ndc.ops.usace.army.mil/ords/lpms/lock_delay_json"
    
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to fetch data. HTTP Status Code: {response.status_code}"

@st.cache_data
def fetch_lock_status_report(in_river_code):
    base_url = f"https://ndc.ops.usace.army.mil/ords/lpms/lock_status_report_json?in_river_code={in_river_code}"

    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to fetch data. HTTP Status Code: {response.status_code}"

@st.cache_data
def fetch_tonnage_report(in_river_name, in_lock, in_month_year):

    
    full_url = f"https://ndc.ops.usace.army.mil/ords/lpms/json/monthly_tons_report?in_river_name={in_river_name}&in_lock={in_lock}&in_month_year={in_month_year}"
    # response = requests.get(base_url, params=params)
    response = requests.get(full_url)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to fetch data. HTTP Status Code: {response.status_code}"


@st.cache_data
def fetch_traffic_report(in_river, in_lock):
    base_url = f"https://ndc.ops.usace.army.mil/ords/lpms/json/traffic_report?in_river={in_river}&in_lock={in_lock}"
    
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to fetch data. HTTP Status Code: {response.status_code}"
