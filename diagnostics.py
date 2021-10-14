import pandas as pd
import subprocess
import timeit
import pickle
import os
import json
import sys

# Load config.json and get environment variables
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
test_data_path = os.path.join(config['test_data_path'])
model_path = os.path.join(os.getcwd(), config['output_model_path'])
prod_deployment_path = os.path.join(os.getcwd(), config['prod_deployment_path'])


# Function to get model predictions
def model_predictions(data_file_name=None):
    # read the deployed model and a test dataset, calculate predictions
    with open(os.path.join(prod_deployment_path, 'trainedmodel.pkl'), 'rb') as file:
        model = pickle.load(file)
    if data_file_name is None:
        test_data = os.path.join(test_data_path, 'testdata.csv')
        df = pd.read_csv(test_data)
    else:
        test_data = os.path.join(test_data_path, data_file_name)
        df = pd.read_csv(test_data)

    X = df[["lastmonth_activity", "lastyear_activity", "number_of_employees"]]
    y_pred = model.predict(X)
    predictions = y_pred.tolist()
    print("The prediction(s):")
    print(predictions)

    return predictions


# Function to get summary statistics
def dataframe_summary(dataframe=None,
                      numeric_columns=["lastmonth_activity", "lastyear_activity", "number_of_employees"]):
    # calculate summary statistics here
    if dataframe is None:
        test_data = os.path.join(test_data_path, 'testdata.csv')
        df = pd.read_csv(test_data)
    else:
        df = dataframe

    result = []
    for column in numeric_columns:
        result.append([column, "mean", df[column].mean(),
                       "median", df[column].median(),
                       "standard deviation", df[column].std()])
    print(result)
    return result


# Function to get missing data
def missing_check(dataframe=None,
                  numeric_columns=["lastmonth_activity", "lastyear_activity", "number_of_employees"]):
    if dataframe is None:
        test_data = os.path.join(test_data_path, 'testdata.csv')
        df = pd.read_csv(test_data)
    else:
        df = dataframe

    result = []
    for column in numeric_columns:
        n_missing = df[column].isna().sum()
        percent_missing = df[column].isna().mean()

        result.append([column, n_missing, str(round(percent_missing * 100, 2)) + "%"])

    print(result)
    return result


# Function to get timings
def execution_time():
    # calculate timing of training.py and ingestion.py
    result = []

    start_time = timeit.default_timer()
    os.system('python ingestion.py')
    ingestion_timing = timeit.default_timer() - start_time

    start_time = timeit.default_timer()
    os.system('python training.py')
    training_timing = timeit.default_timer() - start_time

    result.append(ingestion_timing)
    result.append(training_timing)

    print(f"Data ingestion time: {round(ingestion_timing, 2)}s \nModel training time: {round(training_timing, 2)}s")
    return result


# Function to check dependencies
def outdated_packages_list():
    # get a list of
    outdated_list = subprocess.check_output(['pip', 'list', '--outdated']).decode(sys.stdout.encoding)
    print(outdated_list)

    return outdated_list


if __name__ == '__main__':
    model_predictions()
    dataframe_summary()
    missing_check()
    execution_time()
    outdated_packages_list()
