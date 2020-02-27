import numpy as np
from sklearn.ensemble import RandomForestClassifier
from flask_socketio import emit

def execute(forest, test_features):
    """"""

    emit('progressLog', {'message': "Predicting with random forest."})

    predictions = forest.predict(test_features)
    return predictions