from similarity_calculator import SimilarityCalculator
from naive_bayes import NaiveBayes
import constants
import pickle
import sys
import pdb
from collections import OrderedDict

if __name__ == '__main__':
    sc = SimilarityCalculator()
    with open(constants.NB_PKL_FILENAME, 'rb') as f:
        nb_classifier = pickle.load(f)

        nb_input = NaiveBayes()

        for query in sys.stdin:
            nb_input.word_count = {}
            nb_input.train(query, 'input')
            results = OrderedDict()

            for category in nb_classifier.word_count:
                sim_cos = sc.sim_cos(nb_input.word_count['input'], nb_classifier.word_count[category])
                results[category] = sim_cos

            for result in results:
                print('カテゴリ「%s」との類以度は %f です' % (result, results[result]))

            best_score_before = 0.0
            best_category = ''
            
            for i, category in enumerate(results):
                if results[category] > best_score_before:
                    best_category = category
                    best_score_before = results[category]
            try:
                print('類以度の最も高いカテゴリは「%s」で、類以度は %f です' % (best_category, results[best_category]))
            except KeyError:
                continue
