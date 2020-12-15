from typing import List, Dict, Tuple, Optional

import spacy
from spacy.lang.fr import French as SpacyModel
from spacy.util import minibatch, compounding


def format_data_as_spacy(raw_data: List[Dict[str, str]]) -> Tuple[List[str], List[Dict[str, bool]]]:
    """
    Format the raw_data as the format expected by spacy.

    Parameters
    -----------
    - **raw_data**: the dataset to be formatted.

    Return
    ----------
    A Tuple containing the texts and labels in spacy format.
    The texts are a list of sentences.
    The labels are a list of Dict where each Dict has all labels as keys and a bool.
    saying if it belongs or not to given class.
    """

    texts = [td['sentence'] for td in raw_data]
    labels = [td['intent'] for td in raw_data]

    cats = [{'find-around-me': y == 'find-around-me',
             'purchase': y == 'purchase',
             'find-hotel': y == 'find-hotel',
             'provide-showtimes': y == 'provide-showtimes',
             'irrelevant': y == 'irrelevant',
             'find-train': y == 'find-train',
             'find-flight': y == 'find-flight',
             'find-restaurant': y == 'find-restaurant'} for y in labels]

    return texts, cats


def get_spacy_model(labels: List[str]) -> SpacyModel:
    """
    Get a trainable classifier SpacyModel for given possible labels.

    Return
    ----------
    The spacy model.
    """

    nlp = spacy.load('fr_core_news_sm')

    textcat = nlp.create_pipe("textcat", config={"exclusive_classes": True, "architecture": "ensemble"})
    nlp.add_pipe(textcat, last=True)

    for label in labels:
        textcat.add_label(label)

    return nlp


def train(model: SpacyModel, X: List[str], y: List[Dict[str, bool]], n_iter: int = 10,
          test: Optional[Tuple[List[str], List[Dict[str, bool]]]] = None) -> SpacyModel:
    """
    Re-train the given space model with the texts and labels passed.

    Parameters
    -----------
    - **model**: the model to retrain.
    - **X**: the texts inputs.
    - **y**: labels.
    - **n_iter**: (*optional*) the amount of iterations to train for(epochs).
    - **test**: (*optional*) the test data set to get the test scores

    Return
    ----------
    The retrained spacy model.
    """

    train_data = list(zip(X, [{"cats": cats} for cats in y]))
    if test:
        test_data = list(zip(test[0], [{"cats": cats} for cats in test[1]]))
    else:
        test_data = None

    # get names of other pipes to disable them during training
    pipe_exceptions = ["textcat", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in model.pipe_names if pipe not in pipe_exceptions]
    with model.disable_pipes(*other_pipes):  # only train textcat
        optimizer = model.begin_training()

        print("Training the model...")

        batch_sizes = compounding(4.0, 32.0, 1.001)
        for i in range(n_iter):

            losses = {}
            # batch up the examples using spaCy's minibatch

            batches = minibatch(train_data, size=batch_sizes)
            for batch in batches:
                texts, annotations = zip(*batch)
                model.update(texts, annotations, sgd=optimizer, drop=0.2, losses=losses)

            scores = model.evaluate(test_data).scores
            if test:
                textcat_score = scores["textcat_score"]
                print(f'Iteration {i}/{n_iter}. train_loss: {losses["textcat"]} test score:{textcat_score}%')
            else:
                print(f'Iteration {i}/{n_iter}. train_loss: {losses["textcat"]}')

    return model


def predict(model: SpacyModel, X: List[str]) -> List[str]:
    """
    Predict the label for each text.

    Parameters
    -----------
    - **model**: the model to use.
    - **X**: the texts inputs.

    Return
    ----------
    A List containing the label of each text.
    """

    prediction = []
    for text in X:
        prediction.append(model(text).cats)

    return [max(result, key=result.get) for result in prediction]


def predict_with_threshold(model: SpacyModel, X: List[str], threshold: float, default_label: str) -> List[str]:
    """
    Predict the label for each text.
    The labels are given if the associated probability is greater than the thresold.

    Parameters
    -----------
    - **model**: the model to use.
    - **X**: the texts inputs.

    Return
    ----------
    A List containing the label of each text.
    """

    prediction = []
    for text in X:
        prediction.append(model(text).cats)
    ret = []
    for result in prediction:
        pred = max(result, key=result.get)
        if result[pred] >= threshold:
            ret.append(pred)
        else:
            ret.append(default_label)

    return ret
