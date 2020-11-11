import requests

from typing import List
import json

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


def get_intent_probabilities(sentence: str, endpoint: str = 'http://localhost:8080/api/intent') -> str:
    """
    Return the probabilities for each intent for the specified sentence.
    """
    r = requests.get(endpoint + '?sentence=' + sentence)
    if r.status_code == 200:
        result = r.json()
    else:
        raise RuntimeError("Couldn't parse sentence")
    return result


def get_most_probable_intent(sentence: str, endpoint: str = 'http://localhost:8080/api/intent') -> str:
    """
    Return the intent with the highest probability for the specified sentence.
    """
    result = get_intent_probabilities(sentence, endpoint)
    return max(result, key=result.get)


def load_json_data(filename: str) -> dict:
    """
    Load the content of the json file as a dict.
    """
    f = open(filename, 'r')
    file_content = json.load(f)
    f.close()
    return file_content


def get_all_intents(endpoint: str = 'http://localhost:8080/api/intent') -> List[str]:
    """
    Send a sample sentence to get a list of all possible intents.
    """
    r = requests.get(endpoint + '?sentence=im a teapot')  # classify anything just to have the labels
    return list(r.json().keys())


def get_raw_training_data(path: str = './training_set.json'):
    """
    Load the raw training set.
    """
    return load_json_data(path)


def get_raw_testing_data(path: str = './testing_set.json'):
    """
    Load the raw testing set.
    """
    return load_json_data(path)


def score(raw_data: dict) -> dict:
    """
    Compute the scores based on the given raw JSON dataset.

    The output dict contains two keys:
        - 'report': which is a classification report given by scikit learn
        - 'cm': which is a confusion matrix not normalized
    """
    y_true = [message['intent'] for message in raw_data]
    y_pred = [get_most_probable_intent(message['sentence']) for message in raw_data]
    labels = get_all_intents()
    return {
        'report': classification_report(y_true, y_pred),
        'cm': confusion_matrix(y_true, y_pred, labels=labels)
    }


def limit_intent(raw_data: dict, intent: str, max_qty: int) -> dict:
    """
    Limit the number of specified intent in the data set.
    """
    current = 0
    output = []
    for message in raw_data:
        if message["intent"] == intent:
            if current < max_qty:
                current += 1
                output.append(message)
        else:
            output.append(message)
    return output
