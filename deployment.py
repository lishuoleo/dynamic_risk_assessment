import os
import json
import shutil


with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(os.path.join(os.getcwd(), config['output_folder_path']))
prod_deployment_path = os.path.join(os.path.join(os.getcwd(), config['prod_deployment_path']))
model_path = os.path.join(os.getcwd(), config['output_model_path'])


# function for deployment
def deploy_model_to_production():
    # copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory
    model_file_name = 'trainedmodel.pkl'
    model_score_file_name = 'latestscore.txt'
    ingestion_record_file_name = 'ingestedfiles.txt'

    model_file = os.path.join(model_path, model_file_name)
    model_score_file = os.path.join(model_path, model_score_file_name)
    ingestion_record_file = os.path.join(dataset_csv_path, ingestion_record_file_name)

    model_deployment_file = os.path.join(prod_deployment_path, model_file_name)
    model_score_deployment_file = os.path.join(prod_deployment_path, model_score_file_name)
    ingestion_record_deployment_file = os.path.join(prod_deployment_path, ingestion_record_file_name)

    if not os.path.exists(prod_deployment_path):
        os.mkdir(prod_deployment_path)
        shutil.copy(model_file, model_deployment_file)
        shutil.copy(model_score_file, model_score_deployment_file)
        shutil.copy(ingestion_record_file, ingestion_record_deployment_file)
    else:
        shutil.copy(model_file, model_deployment_file)
        shutil.copy(model_score_file, model_score_deployment_file)
        shutil.copy(ingestion_record_file, ingestion_record_deployment_file)


if __name__ == '__main__':
    deploy_model_to_production()
