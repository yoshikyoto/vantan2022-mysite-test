from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Article
from blog.qiita import QiitaApiClient
from django.http import JsonResponse

def index(request):
    # Article の model を使ってすべての記事を取得する
    # Article.objects.all() は article のリストが返ってくる
    articles = Article.objects.all()

    # qiita API へのリクエスト処理を追加
    qiita_api = QiitaApiClient()
    qiita_articles = qiita_api.get_django_articles()
    print(qiita_articles)

    # こうすることで、article 変数をテンプレートにわたす事ができる
    # {テンプレート上での変数名: 渡す変数}
    return render(request, "blog/index.html", {
        "articles": articles,
        "qiita_articles": qiita_articles,
    })

def detail(request):
    return HttpResponse("detail page")


class AccountCreateView(View):
    def get(self, request):
        return render(request, "blog/register.html")

    def post(self, request):
        # ユーザー情報を保存する
        User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"],
        )
        # 登録完了画面を表示する
        return render(request, "blog/register_success.html")


class AccountLoginView(LoginView):
    """ログインページのテンプレート"""
    template_name = 'blog/login.html'

    def get_default_redirect_url(self):
        """ログインに成功した時に飛ばされるURL"""
        return "/blog"


class AccountLogoutView(LogoutView):
    template_name = 'blog/logout.html'


class MypageView(LoginRequiredMixin, View):
    login_url = '/blog/login'

    def get(self, request):
        articles = Article.objects.filter(user=request.user)
        return render(request, "blog/mypage.html", {
            "articles": articles
        })


class ArticleCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "blog/article_new.html")

class MypageArticleView(LoginRequiredMixin, View):
    def post(self, request):
        """新しく記事を作成する"""
        # リクエストで受け取った情報をDBに保存する
        article = Article(
            title=request.POST["title"],
            body=request.POST["body"],
            # user には、現在ログイン中のユーザーをセットする
            user=request.user,
        )
        article.save()
        return render(request, "blog/article_created.html")

# 記事一覧を表示する View
class ArticleListView(View):
    def get(self, request):
        # Django の機能である model を使ってすべての記事を取得する
        # articles は article のリストになる
        articles = Article.objects.all()

        # 取得した記事一覧をテンプレートにわたす
        # こうすると、テンプレートの中で articles という変数が渡せる
        return render(request, "blog/articles.html", {
            "articles": articles
        })

# 記事についての View
class ArticleView(View):
    # urls.py の <id> が、 id に入る
    def get(self, request, id):
        # get は条件に合致した記事を一つ取得する
        article = Article.objects.get(id=id)
        return render(request, "blog/article.html", {
            "article": article,
        })

# 記事編集ページを表示する view
class MypageArticleIdEditView(View):
    def get(self, request, id):
        article = Article.objects.get(id=id)
        return render(request, "blog/article_edit.html", {
            "article": article,
        })

class ArticleApiView(View):
    
    def get(self, request):
        # DB から Article を取得
        # articles は blog.models.Article のリスト
        articles = Article.objects.all()

        # Article オブジェクトのリストを、dict の list に変換
        dict_articles = []
        for article in articles:
            dict_article = {
                "id": article.id,
                "title": article.title,
                "body": article.body,
            }
            dict_articles.append(dict_article)

        json = {
            "articles": dict_articles,
        }
        return JsonResponse(json)
