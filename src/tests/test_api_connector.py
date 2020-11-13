from ..api_connector import get_intent_probabilities, get_most_probable_intent, get_all_intents, api_score
from .mocks import test_sentences, test_dataset


ENDPOINT = "http://localhost:8080/api/intent"


def test_get_intent_probabilities():
    for intent, sentence in test_sentences.items():
        result = get_intent_probabilities(sentence, ENDPOINT)
        assert abs(sum([r for r in result.values()]) - 1) <= 10**(-5)


def test_get_most_probable_intent():
    for intent, sentence in test_sentences.items():
        assert get_most_probable_intent(sentence, ENDPOINT) in test_sentences.keys()


def test_get_all_intents():
    for i in get_all_intents(ENDPOINT):
        assert i in test_sentences.keys()


def test_api_score():
    output = api_score(test_dataset)
    assert isinstance(output['report'], str)
    cm = output['cm']
    size = len(test_sentences.keys())
    assert cm.shape == (size, size)
