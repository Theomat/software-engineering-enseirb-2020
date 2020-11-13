from .metrics import score

import requests

from typing import List, Dict


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
    return sorted(list(r.json().keys()))


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


def api_score(raw_data: List[Dict[str, str]], endpoint: str = 'http://localhost:8080/api/intent') -> dict:
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

    return score(y_true, y_pred)
