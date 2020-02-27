import numpy as np
from sklearn.model_selection import train_test_split
from flask_socketio import emit

def execute(dataframe, label_column, random_state=None):
    """"""

    emit('progressLog', {'message': "Splitting data into testing and training set."})

    labels = dataframe[label_column].astype(str)
    features = np.array(dataframe.drop(label_column, axis=1))

    # Split the data into training and testing sets
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.30, random_state=random_state)
    return [train_features, test_features, train_labels, test_labels]