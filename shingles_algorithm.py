import re
from pprint import pprint
from hashlib import sha256, sha384, sha224, sha512, sha1, md5
from typing import Generator
from nltk import ngrams


class CheckDuplicates:
    def __init__(self, length=5):
        self.length = length

    def shingles(self, doc: str) -> Generator[tuple, None, None]:
        assert len(doc) > self.length, 'Please change shingles length'
        return ngrams(self.__text_canonizing(doc).split(), self.length)

    def hash_shingles(self, doc: str) -> list:
        return self.__make_hash(self.shingles(doc))

    @staticmethod
    def __text_canonizing(text: str) -> str:
        return re.sub("[,.!?:;*^%$#]", " ", text)

    @staticmethod
    def __make_hash(ngrams: Generator) -> list:
        hash_ngrams = []
        hash_func = [sha256, sha384, sha224, sha512, sha1, md5]
        ngrams = list(ngrams)
        for func in hash_func:
            hash_ngrams.append([func(' '.join(ngram).encode('utf-8')).hexdigest()
                                for ngram in ngrams])
        return hash_ngrams

    def hash_shingles_similarity(self, text_a: str, text_b: str) -> float:
        count = 0
        hash_text_a, hash_text_b = self.hash_shingles(text_a), self.hash_shingles(text_b)
        for hash_a, hash_b in zip(hash_text_a, hash_text_b):
            if min(hash_a) == min(hash_b):
                count += 1
        return count / len(hash_text_a)



text_a = "Стала стабильнее экономическая и политическая обстановка, предприятия вывели из тени зарплаты сотрудников."
text_b = "Стала стабильнее экономическая и политическая обстановка"
# text_b = "Надеюсь, я доступно смог изложить теорию нахождения почти дубликатов для веб-документов"

checker = CheckDuplicates(5)
print(checker.hash_shingles_similarity(text_a, text_b))


