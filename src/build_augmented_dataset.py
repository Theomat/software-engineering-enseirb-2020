from src.dataset import get_raw_training_data
import os
import json
import functools
from typing import List, Dict

import spacy
from spacy.lang.fr.stop_words import STOP_WORDS


import numpy as np

# =============================================================================
# Globals
seed: int = 1
probs: np.ndarray = np.array([.5, .25, .15, .05, .03, .02])
classes_to_change: List[str] = ["VERB", "NOUN"]
DEBUG: bool = False
# =============================================================================
# Checkup on values
assert np.sum(probs) == 1, f"Probabilities sum={np.sum(probs)}"
# =============================================================================
# Load the model and the training set
print("Loading model...")
nlp = spacy.load("fr_core_news_lg")
vocabulary: List[str] = list(nlp.vocab.strings)
print("Full Vocabulary size:", len(vocabulary))
raw_training_data = get_raw_training_data('./data/training_set.json')
# Create a generator to use for random numbers
generator: np.random.Generator = np.random.default_rng(seed)


new_examples_per_class: Dict[str, int] = {
    "purchase": 187,
    "find-around-me": 217,
    "find-flight": 142,
    "find-hotel": 184,
    "find-restaurant": 231,
    "find-train": 157,
    "provide-showtimes": 183,
}

# =============================================================================
print("Filtering vocabulary...")
print("\tTransforming words into tokens...")
nlp.max_length = 1000000
filtered_words = []
if os.path.exists("./vocab.json"):
    print("\tReusing vocabulary...")
    with open("./vocab.json", "r") as fp:
        words = json.load(fp)
    for i in range(0, len(words), 50000):
        tokens = " ".join([w for w in words[i:min(len(words) - 1, i + 50000)]])
        tokens = nlp(tokens)
        for token in tokens:
            filtered_words.append(token)
else:
    print("\tComputing vocabulary...")
    for i in range(0, len(vocabulary), 50000):
        tokens = " ".join([w for w in vocabulary[i:min(len(vocabulary) - 1, i + 50000)] if w not in STOP_WORDS])
        tokens = nlp(tokens)
        filtered_words += np.unique([w for w in tokens if w.pos_ in classes_to_change and w.is_lower]).tolist()
    with open("./vocab.json", "x") as fp:
        json.dump([w.text for w in filtered_words], fp)
print(f"Filtered vocabulary size:{len(filtered_words)}")

# =============================================================================
cache = {}


@functools.lru_cache(maxsize=-1)
def get_synonyms(lemma, n=10):
    if lemma in cache:
        return cache[lemma]
    lexeme = nlp.vocab[lemma]
    similarity = sorted(filtered_words, key=lambda w: lexeme.similarity(w), reverse=True)
    if DEBUG:
        print([(w.orth_, lexeme.similarity(w)) for w in similarity[:n]])

    out = [w.text for w in similarity[:n]]
    cache[lemma] = out
    return out


# =============================================================================
# Augment the dataset
data = raw_training_data
# 1] Sort sentences by class
sentences: Dict[str, List[str]] = {}
for pt in data:
    intent = pt['intent']
    msg = pt['sentence']
    li = sentences.get(intent, [])
    li.append(msg)
    sentences[intent] = li

# 2] Choose random sentences to be augmented
selected: Dict[str, List[str]] = {}
for intent, nb in new_examples_per_class.items():
    selected[intent] = [str(x) for x in generator.choice(sentences[intent], size=nb)]

# 3] Augment the sentences by replacing some words
new_sentences: List[Dict[str, str]] = []
for intent, sentences in selected.items():
    for sentence in sentences:
        new_sentence = ""
        for word in nlp(sentence):
            # Change only if the word is in the correct class
            if word.pos_ in classes_to_change and word.has_vector:
                lemma: str = word.lemma_
                # Find n + 1 most similar
                # n + 1 because the most similar vector to a vector v is v itself !
                synonyms: List[str] = get_synonyms(lemma, 1 + probs.shape[0])
                if DEBUG:
                    print(f"Synonyms of {word.text}:")
                    for synonym in synonyms:
                        print(f"\t{synonym}")
                # We chose according to the specified probability one vector
                new_lemma = generator.choice(synonyms[1:], p=probs)
                if DEBUG:
                    print("Chosen synonym:", new_lemma, "for", word.text)
                new_sentence += new_lemma
            else:
                new_sentence += word.text
            new_sentence += " "
        new_sentences.append({"intent": intent, "message": new_sentence})
        if DEBUG:
            print("intent=", intent, "old_sentence=", sentence)
            print("intent=", intent, "new_sentence=", new_sentence)
    print("Finished augmenting ", intent)

# =============================================================================
augmented_training_set = new_sentences + data
generator.shuffle(augmented_training_set)

# =============================================================================
# Save the new dataset
with open("../data/augmented_training_set.json", "x") as f:
    json.dump(augmented_training_set, f)

print("Success the new dataset is in data/augmented_training_set.json !")
