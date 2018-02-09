import re
import json
import os
import codecs

def tokenize(doc):
    doc = re.sub("(\w)([.,?!]+)(\w)", r"\1 \2 \3", doc.lower())
    doc = re.sub("(\w)([.,?!]+)$", r"\1 \2", doc)
    doc = re.sub("(\w)'(\w)", r"\1' \2", doc)
    doc = re.sub(" {2,}", " ", doc)
    return doc.split(" ")


def sentiment(data, message):
    tokens = tokenize(message)
    score = 0
    words = []
    positive = []
    negative = []

    negations = {"senza", "non", "niente", "nulla", "meno"}

    for pos, token in enumerate(tokens):
        previous = tokens[pos - 1] if pos > 0 else ""
        negation = -1 if previous in negations else 1
        item = data.get(token)
        if item is None:
            continue
        words.append(token)
        positive.append(token) if item > 0 else negative.append(token)
        score += item * negation

    result = {
        "score": score,
        "comparative": score / float(len(tokens)) if len(tokens) > 0 else 0,
        "vote": "neutral",
        "tokens": tokens,
        "positive": positive,
        "negative": negative,
    }
    if score > 0:
        result["vote"] = "positive"
    if score < 0:
        result["vote"] = "negative"

    return result


def load():
    dataFile = os.path.join(os.path.dirname(__file__), ".", "word_polarities.json")
    with codecs.open(dataFile, encoding='utf-8') as f:
        return json.load(f)

if __name__ == '__main__':
    polarities = load()
    comment = "non sei bravo"
    comment1 = "Infatti hanno ristretto tutte le strade con questi grandi marciapiedi angolari assurdi che hanno tolto e stanno togliendo parcheggio! Automobilisti Poveri noi!!!! ".strip()
    comment2 = "è una presa per il culo!"
    comment3 = "è interessante"
    print(sentiment(polarities, comment))
    print(sentiment(polarities, comment1))
    print(sentiment(polarities, comment2))
    print(sentiment(polarities, comment3))


