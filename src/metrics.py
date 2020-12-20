from typing import List

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import cohen_kappa_score


def score(y_true: List[str], y_pred: List[str]) -> dict:
    """
    Compute the scores based on two results vectors.

    Parameters
    -----------
    - **y_true**: the labels ground truth.
    - **y_pred**: the predicted labels.

    Return
    ----------
    The output dictionnary contains two keys:
        - 'report': which is a classification report given by scikit learn
        - 'cm': which is a confusion matrix not normalized
        - 'kappa': which gives a scalar representing Cohen's kappa score
    """

    labels = sorted(list(set(y_true)))
    return {
        'report': classification_report(y_true, y_pred, zero_division=0),
        'cm': confusion_matrix(y_true, y_pred, labels=labels),
        'kappa': cohen_kappa_score(y_true, y_pred)
    }
