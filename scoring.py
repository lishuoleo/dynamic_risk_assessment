import pandas as pd
import pickle
import os
from sklearn import metrics
import json

# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

model_path = os.path.join(os.getcwd(), config['output_model_path'])
test_data_path = os.path.join(os.getcwd(), config['test_data_path'])


# Function for model scoring
def score_model(model_directory):
    # this function should take a trained model, load test data, and calculate an F1 score for the model relative to
    # the test data
    with open(os.path.join(model_directory, 'trainedmodel.pkl'), 'rb') as file:
        model = pickle.load(file)

    test_data = os.path.join(test_data_path, 'testdata.csv')
    df = pd.read_csv(test_data)
    X = df.drop(['corporation', 'exited'], axis=1)
    y = df.pop('exited')

    y_pred = model.predict(X)

    f1 = metrics.f1_score(y, y_pred)

    # it should write the result to the latestscore.txt file
    my_file = open(os.path.join(model_directory, 'latestscore.txt'), 'w')
    my_file.write(str(f1))

    return f1


if __name__ == '__main__':
    score_model(model_directory=model_path)
