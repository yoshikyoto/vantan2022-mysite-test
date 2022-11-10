import requests

class QiitaApiClient:
    """Qiita の API を叩く役割を持つクラス"""

    def get_django_articles(self):
        # get リクエストを送る
        response = requests.get(
            "https://qiita.com/api/v2/tags/django/items",
            headers={"Authorization": "Bearer c40e213d7c29e8fc239c0d0390b4bd8db6644c7f"},
        )

        qiita_articles = []
        json = response.json()
        for json_article in json:
            qiita_article = QiitaArticle(
                json_article["title"],
                json_article["url"],
            )
            qiita_articles.append(qiita_article)
        return qiita_articles


class QiitaArticle:

    def __init__(self, title, url):
        self.title = title
        self.url = url
