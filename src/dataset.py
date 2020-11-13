from typing import List, Dict
import json


def load_json_data(filename: str) -> dict:
    """
    Load the content of the JSON file as a dict.

    Parameters
    -----------
    - **filename**: the path to the JSON file to be loaded.

    Return
    -----------
    A dictionnary containing the contents of the specified file.
    """
    f = open(filename, 'r')
    file_content = json.load(f)
    f.close()
    return file_content


def get_raw_training_data(path: str = '../data/training_set.json') -> List[Dict[str, str]]:
    """
    Load the content of the raw training data.

    Parameters
    -----------
    - **path**: (*optional*) the path to the dataset.

    Return
    -----------
    A List of dictionnaries.
    Each dictionnary has two keys 'intent' and 'sentence'.
    'intent' has a str value which is the intent-class.
    'sentence' has a str value which is the sentence.
    """
    return load_json_data(path)


def get_raw_testing_data(path: str = '../data/testing_set.json') -> List[Dict[str, str]]:
    """
    Load the content of the raw testing data.

    Parameters
    -----------
    - **path**: (*optional*) the path to the dataset.

    Return
    -----------
    A List of dictionnaries.
    Each dictionnary has two keys 'intent' and 'sentence'.
    'intent' has a str value which is the intent-class.
    'sentence' has a str value which is the sentence.
    """
    return load_json_data(path)


def get_labels(raw_data: List[Dict[str, str]]) -> List[str]:
    """
    Get all labels of a raw dataset.

    Parameters
    -----------
    - **raw_data**: the raw data.

    Return
    -----------
    The list of all possible labels.
    """
    return sorted(list(set([v['intent'] for v in raw_data])))
