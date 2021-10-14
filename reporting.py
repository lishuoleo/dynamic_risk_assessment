import pandas as pd
from sklearn import metrics
import matplotlib.pyplot as plt
import json
import os
from diagnostics import model_predictions

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
test_data_path = os.path.join(config['test_data_path'])
prod_deployment_path = os.path.join(os.path.join(os.getcwd(), config['prod_deployment_path']))

# dataset_csv_path = os.path.join(os.path.join(os.getcwd(), config['output_folder_path']))
# df = pd.read_csv(os.path.join(dataset_csv_path, 'finaldata.csv'))


# Function for reporting
def model_report(dataframe=None):
    # calculate a confusion matrix using the test data and the deployed model
    # write the confusion matrix to the workspace
    if dataframe is None:
        test_data = os.path.join(test_data_path, 'testdata.csv')
        df = pd.read_csv(test_data)
        y = df.pop('exited')
        y_pred = model_predictions(dataframe=None)
    else:
        df = dataframe
        y = df.pop('exited')
        y_pred = model_predictions(df)

    df_cm = metrics.confusion_matrix(y, y_pred)
    f1 = metrics.f1_score(y, y_pred)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.matshow(df_cm, cmap=plt.cm.Oranges, alpha=0.8)
    for i in range(df_cm.shape[0]):
        for j in range(df_cm.shape[1]):
            ax.text(x=j, y=i, s=df_cm[i, j], va='center', ha='center', size='xx-large')

    plt.xlabel('Predictions', fontsize=15)
    plt.ylabel('Actuals', fontsize=15)
    plt.title(f"Confusion Matrix (F1 Score: {round(f1,2)})", fontsize=18)
    plt.savefig(os.path.join(prod_deployment_path, "confusionmatrix.png"))


if __name__ == '__main__':
    model_report(dataframe=None)
