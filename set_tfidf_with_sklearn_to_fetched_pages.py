import utils
import constants
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer

def is_bigger_than_min_tfidf(term, terms, tfidfs):

    '''
    [term for term in terms if is_bigger_than_min_tfidf(term, terms, tfidfs)]で使う
    list化した、語たちのtfidfの値のなかから、順番に当てる関数。
    tfidfの値がMIN_TFIDFよりも大きければTrueを返す
    '''
    if tfidfs[terms.index(term)] > constants.MIN_TFIDF:
        return True
    return False

def tfidf(pages):
    vectorizer = TfidfVectorizer(analyzer = utils.stems, min_df = 1, max_df = 50)
    corpus = [page.text for page in pages]

    x = vectorizer.fit_transform(corpus)

    terms = vectorizer.get_feature_names()
    tfidfs = x.toarray()[constants.DOC_NUM]
    print([term for term in terms if is_bigger_than_min_tfidf(term, terms, tfidfs)])

    print('合計%i種類の単語が%iページから見つかりました。' % (len(terms), len(pages)))

if __name__ == '__main__':
    utils.go_to_fetched_pages_dir()
    pages = utils.load_all_html_files()
    tfidf_result, vectorizer = tfidf(pages)

    pkl_tfidf_result_path = os.path.join('..', constants.TFIDF_RESULT_PKL_FILENAME)
    pkl_tfidf_vectorizer_path = os.path.join('..', constants.TFIDF_VECTORIZERPKL_FILENAME)

    with open(pkl_tfidf_result_path, 'wb') as f:
        pickle.dump(tfidf_result, f)
    with open(pkl_tfidf_vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
