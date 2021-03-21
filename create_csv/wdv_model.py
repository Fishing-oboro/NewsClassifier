import csv
import MeCab
from gensim.models import word2vec
import numpy as np


def load_csv(url):
    csv.field_size_limit(1000000000)
    categories = []
    titles = []
    articles = []
    with open(url) as f:
        reader = csv.DictReader(f)
        # 辞書から本文配列を取得 →　articles = type(list)
        for row in reader:
            categories.append(row['category'])
            titles.append(row['title'])
            articles.append(row['sentence'])
    return {'categories': categories,
            'titles': titles,
            'articles': articles}


def load_wv(url="./livedoor.model"):
    return word2vec.Word2Vec.load(url)


def wv_mean(text, model, surface=False):
    if surface is False:
        mecab = MeCab.Tagger('-O wakati')
        mecab.parse('')
        words = mecab.parse(text).split(' ')
    else:
        mecab = MeCab.Tagger('-Ochasen')
        mecab.parse('')
        if len(text) == 0:
            return None
        words = []
        token = mecab.parse(text).split('\n')
        for ele in token:
            elements = ele.split('\t')
            if elements[0] == "EOS":
                break
            words.append(elements[0])

    wvecs = np.array([model.wv[word] for word in words if word in model.wv.vocab.keys()])
    return np.mean(wvecs, axis=0)


class LiveDoorWVModel:
    def __init__(self, url='./sample.csv'):
        self.data = load_csv(url)
        self.corpus = self.get_corpus()
        self.wv = None

    def get_corpus(self, surface=False):
        corpus = []
        if surface is False:
            mecab = MeCab.Tagger('-Owakati')
            mecab.parse('')
            for i, article in enumerate(self.data['articles']):
                try:
                    wakati = mecab.parse(article).split(' ')
                    corpus.append(wakati)
                except AttributeError:
                    print(str(i) + 'error')
                    self.data['categories'].pop(i)
                    continue
        else:
            mecab = MeCab.Tagger('-Ochasen')
            mecab.parse('')
            for i, article in enumerate(self.data['articles']):
                if len(article) == 0:
                    self.data['categories'].pop(i)
                    continue
                try:
                    words = []
                    token = mecab.parse(article).split('\n')
                    for ele in token:
                        elements = ele.split('\t')
                        if elements[0] == "EOS":
                            break
                        words.append(elements[0])
                    corpus.append(words)
                except AttributeError:
                    self.data['categories'].pop(i)
                    continue
        return corpus

    def create_wv(self, url="./livedoor.model"):
        model = word2vec.Word2Vec(self.corpus)
        model.save(url)
        self.wv = word2vec.Word2Vec.load(url)

    def load_wv(self, url="./livedoor.model"):
        self.wv = word2vec.Word2Vec.load(url)

    def get_dv(self):
        if self.wv is None:
            self.create_wv()
        dvecs = []
        for i, sentence in enumerate(self.corpus):
            wvecs = np.array([self.wv.wv[word] for word in sentence if word in self.wv.wv.vocab.keys()])
            dvecs.append(np.mean(wvecs, axis=0))
        return dvecs
