from django.urls import path
from rest_framework import routers
from api.views import account, topic, news, collect, recommend, comment

# urlpatterns = [
#     # /api/register/
#     path('register/', account.RegisterView.as_view({"post": "create"})),
# ]


# router = routers.SimpleRouter()
#
# # /api/register/
# #   x-list
# #   x-create
# router.register(r'register', account.RegisterView)
#
# urlpatterns = [
#
# ]
# urlpatterns += router.urls

router = routers.SimpleRouter()
router.register(r'register', account.RegisterView, 'register')

# 创建话题（认证）
router.register(r'topic', topic.TopicView)

# 我的资讯
router.register(r'news', news.NewsView)

# 资讯首页
router.register(r'index', news.IndexView)

# 收藏
router.register(r'collect', collect.CollectView)

# 推荐
router.register(r'recommend', recommend.RecommendView)

# 评论
router.register(r'comment', comment.CommentView)

urlpatterns = [
    # path('register/', account.RegisterView.as_view({"post": "create"})),
    path('auth/', account.AuthView.as_view()),
]

urlpatterns += router.urls
