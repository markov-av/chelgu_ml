import re
from typing import Generator
from hashlib import md5
from nltk import ngrams


class CheckDuplicates:
    def __init__(self, length=10):
        self.length = length

    def get_shingles(self, doc: str) -> Generator[tuple, None, None]:
        assert len(doc) > self.length, 'Please change shingles length'
        return ngrams(self.__text_canonizing(doc).split(), self.length)

    def __text_canonizing(self, text: str) -> str:
        return re.sub("[,.!?:;*^%$#]", " ", text)

    def __make_hash(self, text: str) -> str:
        return md5(text.encode('utf-8')).hexdigest()

    def __hash_similarity(self):
        pass


text = "Стала стабильнее экономическая и политическая обстановка, предприятия вывели из тени зарплаты сотрудников."

checker = CheckDuplicates()
print([i for i in checker.get_shingles(text)])

    