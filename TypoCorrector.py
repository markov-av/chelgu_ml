import re
from collections import defaultdict
import json
from typing import Union
from pprint import pprint


class Corrector:
    def __init__(self, path_to_corpus='data.json'):
        with open(path_to_corpus, 'r') as fp:
            self.corpus = json.load(fp)

    def correct(self, word: str, n: int = 1) -> list:
        similar_words = {}
        word_ngrams = self.__make_ngrams(word)
        if word_ngrams:
            for ngram in word_ngrams:
                try:
                    for similar_word in self.corpus[ngram]:
                        similar_words[similar_word] =\
                            self.distance(word, similar_word)
                except KeyError:
                    continue
        else:
            for similar_word in self.corpus[word_ngrams]:
                similar_words[similar_word] = self.distance(word,
                                                            similar_word)
        return sorted(similar_words.items(), key=lambda x: x[1])[:n]

    @staticmethod
    def __make_ngrams(input: str, n: int = 3) -> Union[list, None]:
        output = []
        for i in range(len(input) - n + 1):
            output.append(input[i:i + n])
        return output if output else None

    @staticmethod
    def distance(a: str, b: str) -> int:
        "Calculates the Levenshtein distance between a and b."
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n, m)) space
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)  # Keep current and previous row, not entire matrix
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]


corrector = Corrector()
print(corrector.correct('мужчена', 10))
# [('мужчина', 1), ('мужчины', 2), ('мужчин', 2), ('мужчину', 2),
# ('мужчинах', 2), ('мужчине', 2), ('мужчинам', 2), ('Мужчина', 2),
# ('сужена', 2), ('мужа', 3)]
