import requests

from typing import List, Dict
import json

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


def get_intent_probabilities(sentence: str, endpoint: str = 'http://localhost:8080/api/intent') -> Dict[str, float]:
    """
    Return the probabilities for each intent for the specified sentence.
    It raises a RuntimeError if the status code to the GET request is anything other than HTTP_OK.

    Parameters
    -----------
    - **sentence**: the sentence whose intent is to be guessed
    - **endpoint**: (*optional*) the intent route to the endpoint, default to localhost route on port 8080.

    Return
    -----------
    A dictionnary where the keys are the intent-class and the values are the probabilities.
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

    Parameters
    -----------
    - **sentence**: the sentence whose intent is to be guessed
    - **endpoint**: (*optional*) the intent route to the endpoint, default to localhost route on port 8080.

    Return
    -----------
    The intent with the highest probability accroding to the endpoint.
    """
    result = get_intent_probabilities(sentence, endpoint)
    return max(result, key=result.get)


def load_json_data(filename: str) -> dict:
    """
    Load the content of the JSON file as a dict.

    Parameters
    -----------
    - **filename**: the path to the JSON file to be loaded

    Return
    -----------
    A dictionnary containing the contents of the specified file.
    """
    f = open(filename, 'r')
    file_content = json.load(f)
    f.close()
    return file_content


def get_all_intents(endpoint: str = 'http://localhost:8080/api/intent') -> List[str]:
    """
    Send a sentence to get a list of all possible intents.

    Parameters
    -----------
    - **endpoint**: (*optional*) the intent route to the endpoint, default to localhost route on port 8080.

    Return
    -----------
    The list of all intent class.
    """
    r = requests.get(endpoint + '?sentence=im a teapot')  # classify anything just to have the labels
    return list(r.json().keys())


def get_raw_training_data(path: str = './training_set.json') -> List[Dict[str, str]]:
    """
    Load the content of the raw training data.

    Parameters
    -----------
    - **path**: (*optional*) the path to the dataset

    Return
    -----------
    A List of dictionnaries.
    Each dictionnary has two keys 'intent' and 'sentence'.
    'intent' has a str value which is the intent-class.
    'sentence' has a str value which is the sentence.
    """
    return load_json_data(path)


def get_raw_testing_data(path: str = './testing_set.json') -> List[Dict[str, str]]:
    """
    Load the content of the raw testing data.

    Parameters
    -----------
    - **path**: (*optional*) the path to the dataset

    Return
    -----------
    A List of dictionnaries.
    Each dictionnary has two keys 'intent' and 'sentence'.
    'intent' has a str value which is the intent-class.
    'sentence' has a str value which is the sentence.
    """
    return load_json_data(path)


def score(raw_data: List[Dict[str, str]], endpoint: str = 'http://localhost:8080/api/intent') -> dict:
    """
    Compute the scores based on the given raw dataset.

    Parameters
    -----------
    - **raw_data**: the dataset to compute metrics on.
    - **endpoint**: (*optional*) the intent route to the endpoint, default to localhost route on port 8080.

    Return
    ----------
    The output dictionnary contains two keys:
        - 'report': which is a classification report given by scikit learn
        - 'cm': which is a confusion matrix not normalized
    """
    y_true = [message['intent'] for message in raw_data]
    y_pred = [get_most_probable_intent(message['sentence'], endpoint) for message in raw_data]
    labels = get_all_intents(endpoint)
    return {
        'report': classification_report(y_true, y_pred, zero_division=0),
        'cm': confusion_matrix(y_true, y_pred, labels=labels)
    }


def limit_intent(raw_data: List[Dict[str, str]], intent: str, max_qty: int) -> List[Dict[str, str]]:
    """
    Limit the number of examples of the specified intent-class in the dataset to the maximum quantity defined.

    Parameters
    -----------
    - **raw_data**: the dataset to be changed.
    - **intent**: the intent class to be limited
    - **max_qty**: the maximum numbers of example of that class allowed.

    Return
    ----------
    A new dataset but with the limited amount of examples for the specified intent class.
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
