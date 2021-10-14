import training
import ingestion
import scoring
import deployment
import diagnostics
import reporting
import json
import os

with open("config.json", "r") as f:
    config = json.load(f)

input_folder_path = os.path.join(os.getcwd(), config["input_folder_path"])
prod_deployment_path = os.path.join(os.getcwd(), config['prod_deployment_path'])
model_path = os.path.join(os.getcwd(), config['output_model_path'])
output_folder_path = os.path.join(os.getcwd(), config['output_folder_path'])

# Check and read new data
# first, read ingestedfiles.txt

current_model_files = []
with open(os.path.join(prod_deployment_path, "ingestedfiles.txt"), "r") as report_file:
    for line in report_file:
        current_model_files.append(line.strip())

# second, determine whether the source data folder has files that aren't listed in ingestedfiles.txt
new_file_count = 0
for file in os.listdir(input_folder_path):
    if os.path.join(file, input_folder_path) not in current_model_files:
        new_file_count += 1

# Deciding whether to proceed, part 1
# if you found new data, you should proceed. otherwise, do end the process here
if new_file_count == 0:
    print("No new input data, ending the process.")
    exit(0)

# Checking for model drift check whether the score from the deployed model is different from the score from the model
# that uses the newest ingested data
ingestion.merge_multiple_dataframe()
ingestion.output_ingestion_record(source_location=input_folder_path,
                                  output_location=output_folder_path)
training.train_model()

new_f1 = scoring.score_model(model_directory=model_path)

with open(os.path.join(prod_deployment_path, "latestscore.txt"), 'r') as f:
    old_f1 = float(f.read())

# Deciding whether to proceed, part 2
# if you found model drift, you should proceed. otherwise, do end the process here

if new_f1 >= old_f1:
    print("No model drift detected, ending the process.")
    exit(0)

# Re-deployment
# if you found evidence for model drift, re-run the deployment.py script
print("Model drift detected, deploying the new model.")
deployment.deploy_model_to_production()

# Diagnostics and reporting
# run diagnostics.py and reporting.py for the re-deployed model
diagnostics.model_predictions()
diagnostics.dataframe_summary()
diagnostics.missing_check()
diagnostics.execution_time()
diagnostics.outdated_packages_list()
reporting.model_report()
