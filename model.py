from collections import Counter, OrderedDict
import pandas as pd
from tqdm import tqdm
import collections


class NgramModel:
    """
    Использование сглаживания Лапласа для поддержки невстреченных ранее
    слов
    """
    def __init__(self):
        self.word_count = 0
        self.N = 2
        self.ngram_counter = {}
        self.__word_in_ngram = {}

    def __create_ngrams(self, s: str, n: int):
        s = s.lower()
        # Break sentence in the token, remove empty tokens
        tokens = [token for token in s.split(" ") if token != ""]
        for ngram in enumerate(zip(*[tokens[i:] for i in range(n)])):
            for token in tokens:
                if any(word in token for word in ngram[-1]):
                    if token in self.__word_in_ngram.keys():
                        self.__word_in_ngram[token] += [" ".join(ngram[-1])]
                    else:
                        self.__word_in_ngram[token] = [" ".join(ngram[-1])]
        # Use the zip function to help us generate n-grams
        # Concatentate the tokens into ngrams and return
        ngrams = zip(*[tokens[i:] for i in range(n)])

        return [" ".join(ngram) for ngram in ngrams]

    def fit(self, text: str, n: int = 2) -> dict:
        for s in text.split('.'):
            ngrams = Counter(self.__create_ngrams(s, n))
            if not self.ngram_counter:
                self.ngram_counter.update(ngrams)
            else:
                for ngram in list(ngrams.keys()):
                    if ngram in self.ngram_counter.keys():
                        self.ngram_counter[ngram] += ngrams.pop(ngram)
                self.ngram_counter.update(ngrams)
        self.word_count = sum(self.ngram_counter.values())
        self.ngram_counter = {k: v for k, v in reversed(sorted(
            self.ngram_counter.items(), key=lambda item: item[1]))}
        return self.ngram_counter

    def probability_phrase(self, text: str, n: int = 2):
        """
                Предсказание вероятности входного предложения
        """
        probability = 0
        for gram in self.__create_ngrams(text, n):
            if gram in self.ngram_counter.keys():
                probability += self.ngram_counter[gram] / self.word_count
            else:
                break
        return round(probability, 4)

    def probability_word(self,
                         text: str,
                         phrases_count: int = 1,
                         without_word: bool = False) -> list:
        """
                Предсказание наиболее вероятных пар ко входному слову
        """
        phrases = []
        text = text.lower()
        for phrase in self.ngram_counter:
            if phrases_count != 0 and text in phrase.split():
                if without_word:
                    phrases.append(phrase.split(text)[-1] if phrase.split(text)[-1] else '')
                    phrases_count -= 1 if phrase.split(text)[-1] else 0
                else:
                    phrases.append(
                        (phrase,
                         round(self.ngram_counter[phrase]
                               / self.word_count, 4))
                    )
                    phrases_count -= 1
            if phrases == 0:
                break
        return phrases if phrases else f"Нет продолжения для слова '{text}'"

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
                    phrases_count=1,
                    without_word=True
                )
                if word == f"Нет продолжения для слова '{text}'":
                    break
                else:
                    continue_phrase.append(word[-1].split()[-1])
            except IndexError:
                break
        return f"{text} {' '.join(continue_phrase)}" if continue_phrase\
            else f"Для фразы '{text}' нет продолжения"

    def print_ngramm(self):
        print(self.ngram_counter)


text = "Использование сглаживания Лапласа для поддержки невстреченных ранее слов"

model = NgramModel()
model.fit(text, 2)
text = "Продолжение входной фразы словами до заданной длины. Использование сглаживания Лапласа"
model.fit(text, 2)
text = "Продолжение входной фразы словами до заданной длины"
model.fit(text, 2)
# model.print_ngramm()
print(model.probability_phrase("Продолжение входной фразы словами"))
print(model.probability_word("фразы"))
print(model.continue_phrase("входной", 3))
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


