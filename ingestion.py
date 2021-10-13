import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

# Load config.json and get input and output paths
with open('config.json', 'r') as f:
    config = json.load(f)

input_folder_path = os.path.join(os.getcwd(), config['input_folder_path'])
output_folder_path = os.path.join(os.getcwd(), config['output_folder_path'])
output_file_name = "finaldata.csv"
ingestion_record_name = "ingestedfiles.txt"
output_file_path = os.path.join(output_folder_path, output_file_name)


# Function for data ingestion
def merge_multiple_dataframe():
    # check for datasets, compile them together, and write to an output file
    df_list = pd.DataFrame(columns=["corporation", "lastmonth_activity", "lastyear_activity",
                                    "number_of_employees", "exited"])

    filenames = os.listdir(input_folder_path)

    for each_filename in filenames:
        df1 = pd.read_csv(os.path.join(input_folder_path, each_filename))
        df_list = df_list.append(df1)

    result = df_list.drop_duplicates()

    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)
        result.to_csv(output_file_path, index=False)
    else:
        result.to_csv(output_file_path, index=False)


# Function for ingestion record keeping
def output_ingestion_record(source_location, data_output_name, output_location, record_name):
    output_name = os.path.join(output_location, record_name)
    source_name = os.path.join(source_location, data_output_name)

    data = pd.read_csv(source_name)
    date_time_obj = datetime.now()
    the_time_now = str(date_time_obj.year) + '-' + str(date_time_obj.month) + '-' + str(date_time_obj.day)

    all_records = ['Output File Location: '+source_location,
                   'Output File Name: '+data_output_name,
                   'Output File Record Size: '+str(len(data.index)),
                   'Output Date: '+the_time_now]

    my_file = open(output_name, 'w')
    for element in all_records:
        my_file.write(str(element) + '\n')


if __name__ == '__main__':
    merge_multiple_dataframe()
    output_ingestion_record(source_location=output_folder_path,
                            data_output_name=output_file_name,
                            output_location=output_folder_path,
                            record_name=ingestion_record_name)
