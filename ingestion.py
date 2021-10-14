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


# Function for data ingestion
def merge_multiple_dataframe():
    # check for datasets, compile them together, and write to an output file
    df_list = pd.DataFrame(columns=["corporation", "lastmonth_activity", "lastyear_activity",
                                    "number_of_employees", "exited"])

    filenames = os.listdir(input_folder_path)

    for each_filename in filenames:
        _df = pd.read_csv(os.path.join(input_folder_path, each_filename))
        df_list = df_list.append(_df)

    result = df_list.drop_duplicates()

    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)
        result.to_csv(os.path.join(output_folder_path, "finaldata.csv"), index=False)
    else:
        result.to_csv(os.path.join(output_folder_path, "finaldata.csv"), index=False)


# Function for ingestion record keeping
def output_ingestion_record(source_location, output_location):
    filenames = os.listdir(source_location)

    with open(os.path.join(output_location, "ingestedfiles.txt"), "w") as report_file:
        for file in filenames:
            report_file.write(file + "\n")


if __name__ == '__main__':
    merge_multiple_dataframe()
    output_ingestion_record(source_location=input_folder_path,
                            output_location=output_folder_path)
