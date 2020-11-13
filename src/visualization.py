import seaborn as sn
import matplotlib.pyplot as plt

import numpy as np


def plot_confusion_matrix(cm, labels, title='Confusion Matrix', fmt="d"):
    """
    Plot the specified confusion matrix with seaborn.
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
