from ..utils import limit_intent
from .mocks import test_sentences, test_dataset


def test_limit_intent():
    output = limit_intent(test_dataset, "irrelevant", 1)
    for intent in test_sentences.keys():
        assert 1 == sum([1 for m in output if m['intent'] == intent])
