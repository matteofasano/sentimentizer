import re
import json
import os
import codecs
import string
from nltk.tokenize import word_tokenize



class sentimentizer:


    def tokenize(doc):
        doc = re.sub("(\w)([.,?!]+)(\w)", r"\1 \2 \3", doc.lower())
        doc = re.sub("(\w)([.,?!]+)$", r"\1 \2", doc)
        doc = re.sub("(\w)'(\w)", r"\1' \2", doc)
        doc = re.sub(" {2,}", " ", doc)

        italian_stopwords =  open('italian_stopwords.txt', 'r').read().split('\n')
        italian_name = open('nomi_italiani.txt', 'r').read().split('\n')
        doc = doc.split(" ")
        for token in doc:
            if token in italian_stopwords or token in italian_name:   #elimina le parole "inutili" per diminuire lo sforzo di computazione
                doc.remove(token)

        return doc



    def get_sentiment(data, message):
        tokens = sentimentizer.tokenize(message)
        score = 0
        words = []
        positive = []
        negative = []
        profanity_string = []

        negations = {"senza", "non", "niente", "nulla", "meno","ne","nè"}
        positive_comparative = {"più","meglio","migliore", "grande"}
        profanity = open('profanity_it.txt', 'r').read().split('\n')


        for pos, token in enumerate(tokens):
            previous = tokens[pos - 1] if pos > 0 else ""
            negation = -1 if previous in negations else 1
            item = data.get(token)
            if item is None:
                continue
            words.append(token)
            positive.append(token) if item > 0 else negative.append(token)
            item = 1+item if previous in positive_comparative and item > 0 else -1 + item  #in caso di comparativo di maggioranza aggiungo 1 punto all'item in modo da accentuare la connotazione positiva o tolgo 1 punto se la parola è gia di per se negativa
            score += item * negation

        for pos, token in enumerate(tokens):
            if token in profanity:
                profanity_string.append(token)
                score = score - 2  #in caso di parola presente in profanity tolgo arbitrariamente 2 punti dallo score per dare una connotazione negativa al contesto

        result = {
            "score": score,
            "comparative": score / float(len(tokens)) if len(tokens) > 0 else 0,
            "vote": "neutral",
            "tokens": tokens,
            "positive": positive,
            "negative": negative,
            "profanity":profanity_string,
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
    comment1 = " Renzi è coglione e un falso che davanti a milioni e milioni di persone in tv aveva detto che se perdeva se ne andava, dicendo che era una questione di DIGNITA'!' la gente mica è scema - M5S tutta la vita "
    comment2 = " Io credo che sei il più credibile fino adesso, perciò devi mantenere l'impegno dopo il 4. L'Italia è nostra e la dobbiamo difendere. " #commento proSalvini
    comment3 = " Prima gli italiani del nord o quelli del sud? Prima quello del Triveneto o quello della Calabria? Dimmi un po quello che salta a Verona o che puzza come il coleroso napoletano? Dai salvini rispondimi... Prima il leghista che appartiene al partito che ha fatto sparire 48 milioni o quello che ha comprato e conservato dei lingotti di oro? Quello a cui pagate le multe delle quote latte con i fondi europei destinati al sud, o quelli che invece continuate a derubare? Per una volta... solo per una... rispondi " #commento controSalvini
    comment4 = " Il tuo stile non ha eguali, unico tra tutti a riportare solo i fatti. Forza Matteo andiamo avanti insieme! "  #commento proRenzi
    comment5 = " Che Dio Ti Benedica Silvio Berlusconi. Siamo italiani e dobbiamo amare il nostro Paese. Sei un esempio per tutti noi! Tornerai Presidente Vincitore come sempre! Tutti uniti a votare Forza Italia se volete cambiare la vostra vita in meglio!" #commento proBerlusconi
    print(sentimentizer.get_sentiment(polarities, comment1))
    print(sentimentizer.get_sentiment(polarities, comment2))
    print(sentimentizer.get_sentiment(polarities, comment3))
    print(sentimentizer.get_sentiment(polarities, comment4))
    print(sentimentizer.get_sentiment(polarities, comment5))




