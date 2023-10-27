import os
import pandas as pd

# def collate_old_data(dir_name):
#     for root, subdirs, files in os.walk(dir_name):
#         # print(root)
#         for sub_dir in subdirs:
#             print(sub_dir)
            
#             csv_files = [f for f in os.listdir(os.path.join(root, sub_dir)) if f.endswith('.xlsx')]
#             print(csv_files)
#             data_frames = [pd.read_excel(os.path.join(root, sub_dir, f)) for f in csv_files]
#             if data_frames:  # Check if there are any data frames to concatenate
#                 combined_df = pd.concat(data_frames).drop_duplicates()
#                 combined_filename = f"{sub_dir}_combined.csv"
#     combined_df.to_csv(os.path.join(root, combined_filename), index=False)



def collate_old_data(dir_name):
    for root, subdirs, files in os.walk(dir_name):
        for sub_dir in subdirs:
            excel_files = [f for f in os.listdir(os.path.join(root, sub_dir)) if f.endswith('.xlsx')]
            data_frames = [pd.read_excel(os.path.join(root, sub_dir, f), engine='openpyxl') for f in excel_files]
            if data_frames:  # Check if there are any data frames to concatenate
                combined_df = pd.concat(data_frames).drop_duplicates()

                combined_df.columns = [col.upper().replace(' ', '_') for col in combined_df.columns]

                combined_filename = f"{sub_dir}_combined.csv"
                combined_df.to_csv(os.path.join(root, combined_filename), index=False)

# Usage:

# collate_old_data('old_lock_data')



locks_of_interest = { "Port Allen":"01" , "Bayou Sorrel":"02", "Leland Bowman":"77", "Calcasieu":"08"}



for lock in locks_of_interest:
    new_data_dir = f"data/lock_queue_delays_{lock}_2023-10-26.csv"
    dir = f"data/lock_queue_delays_{lock}_2023-10-26.csv"

    old_data_dir = f"old_lock_data/{lock}_combined.csv"
    new_data = pd.read_csv(new_data_dir)
    old_data = pd.read_csv(old_data_dir)
    combined_data = pd.concat([new_data, old_data]).drop_duplicates(subset=['VESSEL_NAME', 'ARRIVAL_DATE']).reset_index(drop=True)


    combined_data.to_csv(dir)
    print(combined_data)