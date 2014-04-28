# import urllibだけじゃ動かなかったのでparseまで指定
import urllib.parse
import requests
import sys
import my_api_keys

class Bing(object):
    def __init__(self, api_key=my_api_keys.BING_API_KEY):
        """初期化"""
        self.api_key = api_key

    def web_search(self, query, num_of_results, keys=["Url"], skip=0):
        """Bingから検索する"""
        url = 'https://api.datamarket.azure.com/Bing/Search/Web?'
        max_num = 50
        params = {
                "Query": "'{0}'".format(query),
                "Market": "'ja-JP'"
            }

        request_url = url + urllib.parse.urlencode(params) + "&$format=json"
        results = []

        repeat = int((num_of_results - skip) / max_num)
        remainder = (num_of_results - skip) % max_num

        for i in range(repeat):
            result = self._hit_api(request_url, max_num, max_num * repeat, keys)
            results.extend(result)

        if remainder:
            result = self._hit_api(request_url, remainder, max_num * repeat, keys)
            results.extend(result)

        return results

    def related_queries(self, query, keys=["Title"]):
        """クエリの関連付け？"""
        url = 'https://api.datamarket.azure.com/Bing/Search/RelatedSearch?'
        params = {
                "Query": "'{0}'".format(query),
                "Market": "'ja-JP'"
                }

        request_url = url + urllib.parse.urlencode(params) + "&$format=json"
        results = self._hit_api(request_url, 50, 0, keys)
        return results

    def _hit_api(self, request_url, top, skip, keys):
        """API実行"""
        final_url = "{0}&$top={1}&$skip={2}".format(request_url, top, skip)
        response = requests.get(final_url,
                auth=(self.api_key, self.api_key),
                headers={'User-Agent': 'My API Robot'}).json()

        results = []
        for item in response["d"]["results"]:
            result = {}
            for key in keys:
                result[key] = item[key]
            results.append(result)
        return results

if __name__ == '__main__':
    for query in sys.stdin:
        bing = Bing()
        results = bing.web_search(query=query, num_of_results=50, keys=["Title", "Url"])
        print(results)
