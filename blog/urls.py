from django.urls import path
from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail', views.detail, name='detail'),
    path("register", views.AccountCreateView.as_view(), name="register"),
    path("login", views.AccountLoginView.as_view(), name="login"),
    path("logout", views.AccountLogoutView.as_view(), name="logout"),
    path("mypage", views.MypageView.as_view(), name="mypage"),
    path("mypage/new-article", views.ArticleCreateView.as_view(), name="mypage-new-article"),
    path("mypage/articles", views.MypageArticleView.as_view(), name="mypage-articles"),
#    path("mypage/articles/<id>", views.MypageArticleIdView.as_view(), name="mypage-articles"),
    path("mypage/articles/<id>/edit", views.MypageArticleIdEditView.as_view(), name="article"),

    path("articles/<id>", views.ArticleView.as_view(), name="article"),
]
