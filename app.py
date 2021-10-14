from flask import Flask, session, jsonify, request
import json
import os
from diagnostics import model_predictions, dataframe_summary, missing_check, outdated_packages_list, execution_time
from scoring import score_model

# Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(os.getcwd(), config['output_folder_path'])
production_model_path = os.path.join(os.path.join(os.getcwd(), config['prod_deployment_path']))


# Prediction Endpoint
@app.route("/prediction", methods=['POST', 'OPTIONS'])
def predict():
    # call the prediction function you created in Step 3
    data_file_name = request.json.get('dataset_path')
    y_pred = model_predictions(data_file_name)

    return str(y_pred)  # add return value for prediction outputs


# Scoring Endpoint
@app.route("/scoring", methods=['GET', 'OPTIONS'])
def score():
    # check the score of the deployed model
    model_score = score_model(model_directory=production_model_path)
    return str(round(model_score, 2))  # add return value (a single F1 score number)


# Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET', 'OPTIONS'])
def stats():
    # check means, medians, and modes for each column
    summary = dataframe_summary()
    return str(summary)  # return a list of all calculated summary statistics


# Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET', 'OPTIONS'])
def diagnose():
    # check timing and percent NA values
    execute_time = execution_time()
    miss_data = missing_check()
    outdated_package = outdated_packages_list()
    return f"Execution Time: \n{execute_time} \nMissing Data Summary: \n{miss_data} \nOutdated Packages: \n{outdated_package}"  # add return value for all diagnostics


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
