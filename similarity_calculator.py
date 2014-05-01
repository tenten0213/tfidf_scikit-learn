import math

class SimilarityCalculator():
    def _absolute(self, vector):
        """ベクトルvの長さ(絶対値)を返す"""
        squared_distance = sum([vector[word] ** 2 for word in vector])
        distance = math.sqrt(squared_distance)
        return distance

    def sim_cos(self, v1, v2):
        """
        コサイン類以度
        v1とv2で共通するkeyがあったとき、その値の席を加算していく。2つのベクトルの内積になる
        """
        numerator = 0
        for word in v1:
            if word in v2:
                numerator += v1[word] * v2[word]

        denominator = self._absolute(v1) * self._absolute(v2)

        if denominator == 0:
            return 0
        return numerator / denominator

    def sim_simpson(self, v1, v2):
        intersection = 0
        """
        シンプソン係数
        v1とv2で共通するkeyを数える
        """
        for word in v2:
            if word in v1:
                intersection += 1
        denominator = min(len(v1), len(v2))

        if denominator == 0:
            return 0
        return intersection / denominator

if __name__ == '__main__':
    sc = SimilarityCalculator()
    print('コサイン類以度は' + str(sc.sim_cos({'ライフハック': 1, '骨折': 2}, {'ライフハック': 2, '仕事': 1, '趣味': 1})))
    print('シンプソン係数で計算した類以度は' + str(sc.sim_simpson({'ライフハック': 1, '骨折': 2}, {'ライフハック': 2, '仕事': 1, '趣味': 1})))
