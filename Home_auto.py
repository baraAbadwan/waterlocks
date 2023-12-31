from enum import unique
from fetch_lock_data import fetch_lock_delay, fetch_traffic_report, fetch_lock_queue_data, xml_to_dataframe, json_to_dataframe, fetch_stall_stoppage, fetch_tonnage_report, fetch_lock_status_report
import streamlit as st
import pandas as pd 
import datetime
import base64
import os
from datetime import datetime
st.set_page_config(layout="wide")

def get_latest_date_saved():
    files = [f for f in os.listdir('data') if os.path.isfile(os.path.join('data', f))]
    dates = []
    for file in files:
        parts = file.split('_')
        if len(parts) > 1 and parts[-1].endswith('.csv'):
            try:
                dates.append(datetime.strptime(parts[-1][:-4], '%Y-%m-%d').date())
            except ValueError:
                pass
    return max(dates) if dates else None


def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download csv file</a>'
    return href

st.title('Water Locks Data')

try:
    old_date = get_latest_date_saved()
except:
    old_date = ""


st.write(f'Data last pulled {old_date}')

# Get today's date
today = datetime.now()

# Format today's date as a string
today_str = today.strftime('%Y-%m-%d')

# old_date = ''






# col1, col2 = st.columns([1,4])

locks_of_interest = { "Port Allen":"01" , "Bayou Sorrel":"02", "Leland Bowman":"77", "Calcasieu":"08"}


river_code = "GI"

dfs = {}
dirs = {}
# while today_str is not old_date:
for lock in locks_of_interest:
    save_dir = f'data/lock_queue_delays_{lock}_{today_str}.csv'
    load_dir = f'data/lock_queue_delays_{lock}_{old_date}.csv'
    lock_no = locks_of_interest[lock]
    data = fetch_lock_queue_data(river_code, lock_no)
    df = xml_to_dataframe(data)
    df['LOCK_NAME'] = lock
    try: 
        old_df = pd.read_csv(load_dir)
        df = pd.concat([df, old_df]).drop_duplicates()
    except:
        pass
    df.to_csv(save_dir, index = False)
    # st.write(df)
    dfs[lock] = df
    dirs[lock] = load_dir
    # st.write(df)
    
# st.write(dfs)
df_combo = pd.DataFrame()
for lock in dfs:
    # st.write('-------------------------')
    # st.write(lock)
    dfs[lock] = df
    dirs[lock] = load_dir
    # df['LOCK_NAME'] = lock
    df_combo = pd.concat([df_combo, df])
    # st.markdown(get_csv_download_link(df, load_dir), unsafe_allow_html=True)


combo_dir = f'data/lock_queue_delays_{today_str}.csv'

old_data_df = pd.read_csv('old_lock_data/combined_old_data.csv')
df_combo = pd.concat([df_combo, old_data_df]).drop_duplicates(subset=['VESSEL_NAME', 'ARRIVAL_DATE']).reset_index(drop=True)


st.write('-------------------------')
st.write('Download combined data')
df_combo.to_csv(combo_dir)
st.markdown(get_csv_download_link(df_combo, combo_dir), unsafe_allow_html=True)
