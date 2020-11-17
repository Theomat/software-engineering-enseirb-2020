from dataset import get_raw_training_data

import json
from typing import List, Dict

import spacy

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
raw_training_data = get_raw_training_data('./data/training_set.json')
# Create a generator to use for random numbers
generator: np.random.Generator = np.random.default_rng(seed)

# Count the number of examples per class
counts: Dict[str, int] = {}
for msg in raw_training_data:
    counts[msg['intent']] = counts.get(msg['intent'], 0) + 1

# Compute the number of new examples to make
print("Building new examples:")
max_examples = max(counts.values())
new_examples_per_class: Dict[str, int] = {}
for intent, nb in counts.items():
    if nb < max_examples:
        new_examples_per_class[intent] = max_examples - nb
        print(f"\t{intent} will have {max_examples - nb} new examples")


# =============================================================================
filtered_words = [w for w in nlp.vocab if not w.is_stop and w.is_lower and w.has_vector]
print(f"Vocabulary of {len(filtered_words)} lemmas")


def get_synonyms(lemma, n=10):
    lexeme = nlp.vocab[lemma]
    similarity = sorted(filtered_words, key=lambda w: lexeme.similarity(w), reverse=True)
    if DEBUG:
        print([(w.orth_, lexeme.similarity(w)) for w in similarity[:n]])
    return [w.text for w in similarity[:n]]


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
                lemma = word.lemma_
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

augmented_training_set = new_sentences + data
generator.shuffle(augmented_training_set)


# Save the new dataset
with open("../data/augmented_training_set.json", "x") as f:
    json.dump(augmented_training_set, f)

print("Success the new dataset is in data/augmented_training_set.json !")
