from exo1_utils import get_intent_probabilities, get_most_probable_intent, load_json_data, get_all_intents, score, limit_intent

import json

test_sentences = {
    "irrelevant": "Pouet Pouet, camembert ! ",
    "purchase": "Acheter",
    "find-restaurant": "Trouver un restaurant",
    "find-hotel": "Trouver un hotel",
    "find-around-me": "Trouver le plus proche",
    "find-flight": "Trouver un avion",
    "find-train": "Trouver un train",
    "provide-showtimes": "Veux la météo"
}

test_dataset = [
    {"intent": "irrelevant", "sentence": "L Esclavagisme moderne"},
    {"intent": "purchase", "sentence": "Acheter"},
    {"intent": "find-hotel", "sentence": "Trouver un hotel"},
    {"intent": "find-restaurant", "sentence": "Trouver un restaurant"},
    {"intent": "find-around-me", "sentence": "Trouver autour de moi"},
    {"intent": "find-flight", "sentence": "Trouver un avion"},
    {"intent": "find-train", "sentence": "Trouver un train"},
    {"intent": "provide-showtimes", "sentence": "Vouloir la météo"},
    {"intent": "irrelevant", "sentence": "Dictateur"},
    {"intent": "irrelevant", "sentence": "Master >> Main"}
]


ENDPOINT = "http://localhost:8080/api/intent"


def test_get_intent_probabilities():
    for intent, sentence in test_sentences.items():
        result = get_intent_probabilities(sentence, ENDPOINT)
        assert abs(sum([r for r in result.values()]) - 1) <= 10**(-5)


def test_get_most_probable_intent():
    for intent, sentence in test_sentences.items():
        assert get_most_probable_intent(sentence, ENDPOINT) in test_sentences.keys()


def test_load_json_data(tmp_path):
    filepath = str(tmp_path) + 'Test_data.json'
    with open(filepath, 'w+', encoding='utf-8') as f:
        json.dump(test_sentences, f, indent=4)
    assert load_json_data(filepath) == test_sentences


def test_get_all_intents():
    for i in get_all_intents(ENDPOINT):
        assert i in test_sentences.keys()


def test_score():
    output = score(test_dataset, ENDPOINT)
    assert isinstance(output['report'], str)
    cm = output['cm']
    size = len(test_sentences.keys())
    assert cm.shape == (size, size)


def test_limit_intent():
    output = limit_intent(test_dataset, "irrelevant", 1)
    for intent in test_sentences.keys():
        assert 1 == sum([1 for m in output if m['intent'] == intent])
