import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

# Load config.json and get input and output paths
with open('config.json', 'r') as f:
    config = json.load(f)

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']
output_file_name = "finaldata.csv"
ingestion_record_name = "ingestedfiles.txt"
output_file_path = os.path.join(output_folder_path, output_file_name)


# Function for data ingestion
def merge_multiple_dataframe():
    # check for datasets, compile them together, and write to an output file
    directories = os.path.join(os.getcwd(), input_folder_path)
    df_list = pd.DataFrame(columns=["corporation", "lastmonth_activity", "lastyear_activity",
                                    "number_of_employees", "exited"])

    for directory in directories:
        filenames = os.listdir(os.getcwd() + directory)

        for each_filename in filenames:
            df1 = pd.read_csv(os.getcwd() + directory + each_filename)
            df_list = df_list.append(df1)

    result = df_list.drop_duplicates()

    result.to_csv(output_file_path, index=False)


# Function for ingestion record keeping
def output_ingestion_record(sourcelocation, data_output_name, outputlocation, record_name):

    sourcelocation = './recorddatasource/'
    filename = 'recordkeepingdemo.csv'
    outputlocation = 'records.txt'

    with open(os.path.join(output_folder_path, "ingestedfiles.txt"), "w") as report_file:
        for filename in filenames:
            report_file.write(filename + "\n")


if __name__ == '__main__':
    merge_multiple_dataframe()

