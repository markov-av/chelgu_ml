from collections import Counter, OrderedDict
import re
import pandas as pd
from tqdm import tqdm
import collections


class NgramModel:
    """
    n-gram model
    """
    def __init__(self):
        self.word_count = 0
        self.N = 2
        self.ngram_counter = {}
        self.words = {}

    def __create_ngrams(self, s: str, n: int) -> zip:
        tokens = [token for token in s.lower().split(" ") if token != ""]
        return zip(*[tokens[i:] for i in range(n)])

    def __update_words_dict(self, word) -> int:
        key = 0
        try:
            key = self.words[word]
        except KeyError:
            self.word_count += 1
            self.words[word] = self.word_count
        return key if key else self.word_count

    def fit(self, text: str) -> None:
        text = re.sub("[,.!?:;*^%$#/«»<>)(—]", "", text)
        ngrams = Counter(self.__create_ngrams(text, self.N))
        if ngrams:
            for ngram, count in list(ngrams.items()):
                key = self.__update_words_dict(ngram[1])
                try:
                    self.ngram_counter[ngram[0]]\
                        .update(
                        {key: self.ngram_counter[ngram[0]][key] +
                                   count
                            if key in self.ngram_counter[ngram[0]].keys()
                            else count}
                    )
                except KeyError:
                    self.ngram_counter[ngram[0]] = {key: count}

    def probability_phrase(self, text: str) -> float:
        """
        Предсказание вероятности входного предложения
        """
        probability = 1.0
        for gram in self.__create_ngrams(text, self.N):
            if gram[0] in self.ngram_counter.keys()\
                    and gram[1] in self.ngram_counter[gram[0]]:
                probability *=\
                    self.ngram_counter[gram[0]][gram[1]] /\
                    sum(self.ngram_counter[gram[0]].values())
            else:
                break
        return probability

    def probability_word(self,
                         text: str,
                         phrases_count: int = 1,
                         laplace: bool = False) -> list:
        """
        Предсказание наиболее вероятных пар ко входному слову
        Использование сглаживания Лапласа для поддержки невстреченных ранее
        слов
        """
        text = text.lower()
        try:
            index = list({k: v for k, v in reversed(
                sorted(self.ngram_counter[text].items(),
                       key=lambda item: item[1]))})[:phrases_count]
            return [
                list(self.words.keys())[list(self.words.values()).index(idx)]
                for idx in index
            ]
        except KeyError:
            if laplace:
                return list(self.ngram_counter.values())[:phrases_count]
            else:
                print(f"Нет продолжение для слова '{text}'. "
                      f"Попробуйте использовать сглаживание Лапласа")

    def continue_phrase(self, text: str, phrases_count: int):
        """
        Продолжение входной фразы словами до заданной длины
        """
        continue_phrase = []
        word = text.lower().split()[-1]
        for i in range(phrases_count):
            try:
                word = self.probability_word(
                    text=word[-1].split()[-1] if isinstance(word, list)
                    else word,
                    phrases_count=1
                )
                if word == f"Нет продолжения для слова '{text}'":
                    break
                else:
                    continue_phrase.append(word[-1].split()[-1])
            except IndexError:
                break
        return f"{text} {' '.join(continue_phrase)}" if continue_phrase\
            else f"Для фразы '{text}' нет продолжения"

    @property
    def print_ngramm(self):
        import pprint
        return pprint.pprint(self.ngram_counter)


# text = "Использование сглаживания Лапласа для поддержки невстреченных ранее слов"
# model = NgramModel()
# model.fit(text)
# text = "Продолжение входной фразы словами до заданной длины. Использование сглаживания Лапласа"
# model.fit(text)
# text = "Продолжение входной фразы словами до заданной длины"
# model.fit(text)
# model.fit(text)
# model.print_ngramm
# print(model.words)
# print(model.probability_phrase("Продолжение входной фразы словами"))
# print(model.probability_word("фразы"))
# print(model.continue_phrase("входной", 3))
# df = pd.read_csv('news.csv', sep=';')
# df = df[['news_headline', 'news_body']]
# df['news'] = df['news_headline'] + " " + df['news_body']
# for i, news in tqdm(enumerate(df.news.values)):
#     if i > 100: break
#     print(news)
# for i, news in tqdm(enumerate(df.news.values)):
#     if i > 10: break
#     model.fit(news, 2)
# model.pair_to_word('новости')


