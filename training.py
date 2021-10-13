import pandas as pd
import pickle
import os
from sklearn.linear_model import LogisticRegression
import json

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(os.getcwd(), config['output_folder_path'])
model_path = os.path.join(os.getcwd(), config['output_model_path'])


# Function for training the model
def train_model():
    # use this logistic regression for training
    lr = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                            intercept_scaling=1, l1_ratio=None, max_iter=100,
                            multi_class='auto', n_jobs=None, penalty='l2',
                            random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                            warm_start=False)

    # fit the logistic regression to your data
    df = pd.read_csv(os.path.join(dataset_csv_path, 'finaldata.csv'))
    X = df.drop(['corporation', 'exited'], axis=1)
    y = df.pop('exited')

    lr.fit(X, y)

    # write the trained model to your workspace in a file called trainedmodel.pkl
    model_output_file = os.path.join(model_path, 'trainedmodel.pkl')

    if not os.path.exists(model_path):
        os.mkdir(model_path)
        file_handler = open(model_output_file, 'wb')
        pickle.dump(lr, file_handler)
    else:
        file_handler = open(model_output_file, 'wb')
        pickle.dump(lr, file_handler)


if __name__ == '__main__':
    train_model()
