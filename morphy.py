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
        import os
        print(os.getcwd())
        with open('odict.csv', encoding='cp1251') as f:
            self.odict = f.readlines()
        for line in self.odict:
            lemma, value, *other_words = line.split(',')
            self.corpus[lemma] = {'lemma': lemma, 'value': self.mapper[value]}
            for word in other_words:
                if word in self.corpus.keys():
                    continue
                else:
                    self.corpus[word] = {'lemma': lemma,
                                         'value': self.mapper[value]}

    def __to_lemmatize(self, word: str):
        return self.corpus.get(
            word.lower(), {'lemma': word.lower(), 'value': 'S'}
        )

    def lemmatize(self, text: str) -> str:
        lemmatize_text = ''
        text = re.sub("[,.]", " ", text)
        for word in text.split():
            lemmatize_word = self.__to_lemmatize(word)
            lemmatize_text = f"{lemmatize_text}" + \
                             f"{word}" + \
                             "{" + \
                             f"{lemmatize_word['lemma']}=" + \
                             f"{lemmatize_word['value']}" + \
                             "} "
        return lemmatize_text


text = "Стала стабильнее экономическая и политическая обстановка, предприятия " \
       "вывели из тени зарплаты сотрудников. Все Гришины одноклассники уже " \
       "побывали за границей, он был чуть ли не единственным, кого не вывозили " \
       "никуда дальше Красной Пахры."


morphy = OdictMorphy()
print(morphy.lemmatize(text=text))

test_text = "Стала{стать=V} стабильнее{стабильный=A} экономическая{экономический=A} " \
            "и{и=ADV} политическая{политический=A} обстановка{обстановка=S} " \
            "предприятия{предприятие=S} вывели{вывести=V} из{из=PR} тени{тень=S} " \
            "зарплаты{зарплата=S} сотрудников{сотрудник=S} Все{все=S} Гришины{гришин=A} " \
            "одноклассники{одноклассник=S} уже{узкий=A} побывали{побывать=V} " \
            "за{за=PR} границей{граница=S} он{он=S} был{был=S} чуть{чуть=CONJ} ли{ли=ADV} " \
            "не{не=ADV} единственным{единственный=A} кого{кого=S} не{не=ADV} " \
            "вывозили{вывозить=V} никуда{никуда=ADV} дальше{дальше=ADV} " \
            "Красной{красный=A} Пахры{пахры=S} "