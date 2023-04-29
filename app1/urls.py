
from rest_framework import routers
from app1.views import account, topic, news, collect, recommend
from django.urls import path


router = routers.SimpleRouter()

router.register(r'register', account.RegisterView, "register")
router.register(r'topic', topic.TopicView)
router.register(r'news', news.NewsView)
router.register(r'index', news.IndexView)
router.register(r'collect', collect.CollectView)
router.register(r'recommend', recommend.RecommendView)
urlpatterns = [
    path("auth/", account.AuthView.as_view())
]

urlpatterns += router.urls
