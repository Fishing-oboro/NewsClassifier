import create_csv.wdv_model as wvm
import create_csv.categorize_model as cm
import create_csv.makeholder as mh


def text_categorize(text, title=None, url='statics', surface=False):
    dvec = wvm.wv_mean(
        text,
        model=wvm.load_wv(url='create_csv/livedoor_wv.model'),
        surface=surface
    )
    clf = cm.load_clf(url='create_csv/livedoor_clf.pickle')
    mh.make_file(clf.predict([dvec])[0], text, title, url)
    return clf.predict([dvec])[0]
