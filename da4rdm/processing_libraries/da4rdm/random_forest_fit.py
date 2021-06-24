import numpy as np
from sklearn.ensemble import RandomForestClassifier
from flask_socketio import emit

def execute(train_features, train_labels, random_state=None):
    """"""

    emit('progressLog', {'message': "Fitting random forest."})

    forest = RandomForestClassifier(n_estimators=1000, random_state=random_state)
    forest.fit(train_features, train_labels)

    return forest