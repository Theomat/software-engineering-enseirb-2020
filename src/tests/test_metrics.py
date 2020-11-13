from ..metrics import score
from .mocks import test_sentences, test_dataset


def test_score():
    y = [message['intent'] for message in test_dataset]

    output = score(y, y)
    assert isinstance(output['report'], str)
    cm = output['cm']
    size = len(test_sentences.keys())
    assert cm.shape == (size, size)
