import pandas as pd
from pprint import pprint
import re
import json


def ngrams(input, n):
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output if output else None


corpus = {}
corpus[None] = []
df = pd.read_csv('news.csv', sep=';')
for i, news in enumerate(df['news_body'].values):
    try:
        news = re.sub("[,.!?:;*^%$#/«»<>)(—]", "", news).split()
    except:
        break
    for word in news:
        three_grams = ngrams(word, 3)
        if three_grams:
            for three_gram in three_grams:
                if three_gram in corpus.keys():
                    if word not in corpus[three_gram]:
                        corpus[three_gram].append(word)
                else:
                    corpus[three_gram] = [word]
        else:
            corpus[three_grams].append(word)


with open('data.json', 'w') as fp:
    json.dump(corpus, fp)

with open('data.json', 'r') as fp:
    data = json.load(fp)

print(pprint(data))