from ..dataset import load_json_data, get_labels
from .mocks import test_sentences, test_dataset, all_labels

import json


def test_load_json_data(tmp_path):
    filepath = str(tmp_path) + 'Test_data.json'
    with open(filepath, 'w+', encoding='utf-8') as f:
        json.dump(test_sentences, f, indent=4)
    assert load_json_data(filepath) == test_sentences


def test_get_labels():
    assert get_labels(test_dataset) == all_labels
