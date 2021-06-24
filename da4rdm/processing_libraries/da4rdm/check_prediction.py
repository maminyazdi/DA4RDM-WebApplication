import numpy as np
from flask_socketio import emit
from sklearn.metrics import (recall_score, precision_score, accuracy_score, f1_score, roc_auc_score)

def execute(predictions, test_labels, average='macro'):
    """"""

    emit('progressLog', {'message': "Checking prediciont."})

    #number_true_predictions = np.sum(test_labels==predictions)
    #number_total_predictions = predictions.size
    #recall = number_true_predictions / number_total_predictions

    #recall score
    recall = recall_score(test_labels, predictions, average=average)

    #precision score
    precision = precision_score(test_labels, predictions, average=average)

    #accuracy score
    accuracy = accuracy_score(test_labels, predictions)

    #F1 score
    f1 = f1_score(test_labels, predictions, average=average)

    #AUC score
    #roc_auc = roc_auc_score(test_labels, predictions, average=average)

    return [recall, precision, accuracy, f1]