from sklearn.neural_network import MLPClassifier
import pickle


def create_clf(dvecs, categories, url='model.pickle'):
    clf = MLPClassifier(verbose=True)
    clf.fit(dvecs, categories)
    with open(url, mode='wb') as f:
        pickle.dump(clf, f, protocol=2)


def load_clf(url='model.pickle'):
    with open(url, mode='rb') as f:
        return pickle.load(f)
