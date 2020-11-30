import seaborn as sn
import matplotlib.pyplot as plt

from typing import List
from numbers import Number
from sklearn.metrics import roc_curve

import numpy as np

from api_connector import get_most_probable_intent, get_all_intents


def plot_confusion_matrix(cm: List[List[Number]], labels: List[str], title='Confusion Matrix', fmt="d"):
    """
    Plot the specified confusion matrix with seaborn.

    Parameters
    -----------
    - **cm**: the confusion matrix to be plotted.
    - **labels**: the labels for each row/column.
    """

    plt.figure(figsize=(10, 7))

    ax = sn.heatmap(cm,
                    annot=True,
                    fmt=fmt,
                    cmap="Blues_r",
                    xticklabels=labels,
                    yticklabels=labels)

    ax.yaxis.set_ticklabels(ax.yaxis.get_ticklabels(), rotation=0, ha='right')
    ax.xaxis.set_ticklabels(ax.xaxis.get_ticklabels(), rotation=45, ha='right')

    ax.set(title=title,
           ylabel='Predicted label',
           xlabel='True label')

    plt.show()


def plot_distribution(raw_training_data: dict, raw_testing_data: dict):
    """
    Plot the distribution of raw training and testing data

    Parameters
    -----------
    - **raw_training_data**: the training data.
    - **raw_testing_data**: the testing data.
    """

    intents_training = [msg["intent"] for msg in raw_training_data]
    intents_test = [msg["intent"] for msg in raw_testing_data]
    plt.figure(figsize=((12, 6)))
    ax = plt.subplot(1, 2, 1)
    plt.hist(intents_training, bins=np.arange(9)-0.5, density=True)
    for tick in ax.get_xticklabels():
        tick.set_horizontalalignment('center')
        tick.set_rotation("vertical")
    plt.ylabel("Fraction of examples")
    plt.title("Training set")
    ax = plt.subplot(1, 2, 2)
    plt.hist(intents_test, bins=np.arange(9)-0.5, density=True)
    for tick in ax.get_xticklabels():
        tick.set_horizontalalignment('center')
        tick.set_rotation("vertical")
    plt.ylabel("Fraction of examples")
    plt.title("Test set")
    plt.show()


def print_roc_curve(data):
    """
    Plot the roc curves of raw testing data

    Parameters
    -----------
    - **data**: the testing data.
    """
    endpoint = 'http://localhost:8080/api/intent'
    y_true = [message['intent'] for message in data]
    y_pred = [get_most_probable_intent(message['sentence'], endpoint) for message in data]
    for intent in get_all_intents(endpoint):
        y_t = []
        y_p = []
        for k in range(len(y_true)):
            y_t.append(y_true[k] == intent)
            y_p.append(y_pred[k] == intent)
        fpr, tpr, _ = roc_curve(y_t, y_p)
        plt.plot(fpr, tpr, label=f'{intent}')
    plt.show()
