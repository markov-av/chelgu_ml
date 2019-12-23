import re
from hashlib import md5
from nltk import ngrams


class CheckDuplicates:
    def __init__(self, length=5):
        self.length = length

    def shingles(self, doc: str) -> tuple:
        assert len(doc) > self.length, 'Please change shingles length'
        return ngrams(self.__text_canonizing(doc).split(), self.length)

    def hash_shingles(self, doc: str) -> list:
        return self.__make_hash(self.shingles(doc))

    @staticmethod
    def __text_canonizing(text: str) -> str:
        return re.sub("[,.!?:;*^%$#]", " ", text)

    @staticmethod
    def __make_hash(ngrams: tuple) -> list:
        return [md5(' '.join(ngram).encode('utf-8')).hexdigest()
                for ngram in ngrams]

    def hash_shingles_similarity(self, text_a: str, text_b: str) -> float:
        count = 0
        hash_text_a, hash_text_b = self.hash_shingles(text_a), self.hash_shingles(text_b)
        for hash_a, hash_b in zip(hash_text_a, hash_text_b):
            if hash_a == hash_b:
                count += 1
        return count / len(hash_text_a)



text_a = "Стала стабильнее экономическая и политическая обстановка, предприятия вывели из тени зарплаты сотрудников."
text_b = "Стала стабильнее экономическая и политическая обстановка, предприятия вывели из тени"

checker = CheckDuplicates()
print(checker.hash_shingles_similarity(text_a, text_b))


