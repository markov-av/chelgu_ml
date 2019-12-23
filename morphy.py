import re
from typing import Dict


class OdictMorphy:
    mapper = {
        'межд.': 'ADV',
        'с': 'S',
        'союз': 'CONJ',
        'част.': 'ADV',
        'ж': 'S',
        'м': 'S',
        'п': 'A',
        'мо': 'S',
        'жо': 'S',
        'св-нсв': 'V',
        'н': 'ADV',
        'вводн.': 'ADV',
        'нсв': 'V',
        'мн.': 'S',
        'св': 'V',
        'предл.': 'PR',
        'предик.': 'ADV',
        'мо-жо': 'S',
        'со': 'S',
        'сравн.': 'ADV',
        'мс-п': 'ADV',
        'числ.-п': 'ADV',
        'числ.': 'ADV'
    }

    def __init__(self):
        self.corpus: Dict[str] = dict()
        with open('odict.csv', encoding='cp1251') as f:
            self.odict = f.readlines()
        for line in self.odict:
            lemma, value, *other_words = line.split(',')
            self.corpus[lemma] = {'lemma': lemma, 'value': value}
            for word in other_words:
                if word in self.corpus.keys():
                    continue
                else:
                    self.corpus[word] = {'lemma': lemma, 'value': value}

    def __to_lemmatize(self, word: str) -> dict:
        return self.corpus.get(
            word.lower(), {'lemma': word.lower(), 'value': 'мн.'}
        )

    def lemmatize(self, text: str) -> str:
        lemmatize_text = ''
        for word in re.sub("[,.]", " ", text).split():
            lemmatize_word = self.__to_lemmatize(word)
            lemmatize_text = f"{lemmatize_text}" + \
                             f"{word}" + \
                             "{" + \
                             f"{lemmatize_word['lemma']}=" + \
                             f"{self.mapper[lemmatize_word['value']]}" + \
                             "} "
        return lemmatize_text

 '''
You've got the score 0.7471736896197327 
(86.5% correct lemmas and 81.7% correct POS tags)
'''
# morphy = OdictMorphy()
# with open('dataset_37845_1.txt') as f:
#     data = f.readlines()
# with open('answer.txt', 'w') as f:
#     for text in data:
#         f.write(f"{morphy.lemmatize(text=text)}\n")
