import math
import sys
import MeCab

class NaiveBayes():
    def __init__(self):
        self.vocabularies = set()
        self.category_count = {}
        self.category_count = {}

    def to_words(self, sentence):
        tagger = MeCab.Tagger('mecabrc') # Tagger
        mecab_result = tagger.parse(sentence)
        info_of_words = mecab_result.split('\n')
        words = []

        for info in info_of_words:
            # mecabで分けると分の最後の''が、その手前に'EOS'がくる
            # 6番目には無活用形の単語が入る
            info_elems = info.split(',')

            if info_elems[6] == '*':
                words.append(info_elems[0][:-3]) # '','EOS'の前まで？
                continue
            words.append(info_elems[6])
        return tuple(words)

    def word_count_up(self, word, category):
        self.word_count.setdefault(category, {})
        self.word_count[category].setdefault(word, 0)
        self.word_count[category][word] += 1
        self.vocabularies.add(word)

    def category_count_up(self, category):
        self.category_count.setdefault(category, 0)
        self.category_count[category] +=1

    def train(self, doc, category):
        words = self.to_words(doc)
        for word in words:
            self.word_count_up(word, category)
        self.category_count_up(category)

    def prior_prob(self, category):
        num_of_categories = sum(self.category_count.values())
        num_of_docs_of_the_category = self.category_count[category]
        return num_of_docs_of_the_category / num_of_categories

    def num_of_appearance(self, word, category):
        if word in self.word_count[category]:
            return self.word_count[category][word]
        return 0

    def word_prob(self, word, category):
        # ベイズの法則の計算。通常は非常に0に近い小数になる
        numerator = self.num_of_appearance(word, category) + 1
        # +1は加算スムージングのラプラス法
        denominator = sum(self.word_count[category].values()) + len(self.vocabularies)
        prob = numerator / denominator
        return prob

    def score(self, words, category):
        # logを取るのは、 word_probが0.000.....01くらいの小数になったりするため
        score = math.log(self.prior_prob(category))
        for word in words:
            score += math.log(self.word_prob(word, category))
        return score

    def score_without_log(self, words, category):
        score = self.prior_prob(category)
        for word in words:
            score *= self.word_prob(word, category)
        return score

    def classify(self, doc):
        best_guessed_category = None
        max_prob_before = -sys.maxsize
        words = self.to_words(doc)

        for category in self.category_count.keys():
            prob = self.score(words, category)
            if prob > max_prob_before:
                max_prob_before = prob
                best_guessed_category = category
            return best_guessed_category

if __name__ == '__main__':
    nb = NaiveBayes()
    nb.train('''Python（パイソン）は，オランダ人のグイド・ヴァンロッサムが作ったオープンソースのプログラミング言語。
                オブジェクト指向スクリプト言語の一種であり，Perlとともに欧米で広く普及している。イギリスのテレビ局 BBC が製作したコメディ番組『空飛ぶモンティパイソン』にちなんで名付けられた。
                Python は英語で爬虫類のニシキヘビの意味で，Python言語のマスコットやアイコンとして使われることがある。Pythonは汎用の高水準言語である。プログラマの生産性とコードの信頼性を重視して設計されており，核となるシンタックスおよびセマンティクスは必要最小限に抑えられている反面，利便性の高い大規模な標準ライブラリを備えている。
                Unicode による文字列操作をサポートしており，日本語処理も標準で可能である。多くのプラットフォームをサポートしており（動作するプラットフォーム），また，豊富なドキュメント，豊富なライブラリがあることから，産業界でも利用が増えつつある。
             ''',
             'Python')
    nb.train('''ヘビ（蛇）は、爬虫綱有鱗目ヘビ亜目（Serpentes）に分類される爬虫類の総称。
                体が細長く、四肢がないのが特徴。ただし、同様の形の動物は他群にも存在する。
                ''', 'Snake')
    nb.train('''Ruby（ルビー）は，まつもとゆきひろ（通称Matz）により開発されたオブジェクト指向スクリプト言語であり，
                従来 Perlなどのスクリプト言語が用いられてきた領域でのオブジェクト指向プログラミングを実現する。
                Rubyは当初1993年2月24日に生まれ， 1995年12月にfj上で発表された。
                名称のRubyは，プログラミング言語Perlが6月の誕生石であるPearl（真珠）と同じ発音をすることから，
                まつもとの同僚の誕生石（7月）のルビーを取って名付けられた。
             ''',
             'Ruby')
    nb.train('''ルビー（英: Ruby、紅玉）は、コランダム（鋼玉）の変種である。赤色が特徴的な宝石である。
                天然ルビーは産地がアジアに偏っていて欧米では採れないうえに、
                産地においても宝石にできる美しい石が採れる場所は極めて限定されており、
                3カラットを超える大きな石は産出量も少ない。
             ''', 'Gem')
    doc = 'グイド・ヴァンロッサムが作ったオープンソース'
    print('%s => 推定カテゴリ: %s' % (doc, nb.classify(doc)))  # 推定カテゴリ: Pythonになるはず
    print('Pythonカテゴリである確率: %s' % nb.score_without_log(['グイド・ヴァンロッサム', 'が', '作った'], 'Python'))
    print('Rubyカテゴリである確率: %s' % nb.score_without_log(['グイド・ヴァンロッサム', 'が', '作った'], 'Ruby'))

    doc = 'プログラミング言語のRubyは純粋なオブジェクト指向言語です.'
    print('%s => 推定カテゴリ: %s' % (doc, nb.classify(doc)))  # 推定カテゴリ: Rubyになるはず
    print('Rubyカテゴリである確率: %s' % nb.score_without_log(['プログラミング言語', 'の', 'Ruby', 'は', '純粋', 'な', 'オブジェクト指向言語', 'です', '。'], 'Ruby'))
    print('Pythonカテゴリである確率: %s' % nb.score_without_log(['プログラミング言語', 'の', 'Ruby', 'は', '純粋', 'な', 'オブジェクト指向言語', 'です', '。'], 'Python'))

    doc = 'コランダム'
    print('%s => 推定カテゴリ: %s' % (doc, nb.classify(doc)))  # 推定カテゴリ: Gemになるはず
    print('Gemカテゴリである確率: %s' % nb.score_without_log(['コランダム'], 'Gem'))
    print('Rubyカテゴリである確率: %s' % nb.score_without_log(['コランダム'], 'Ruby'))
