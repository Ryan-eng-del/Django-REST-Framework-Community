from app1.extensions.mixins import DigCreateModelMixin, DigListModelMixin, DigDestroyModelMixin, DigUpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from app1.models import News
from app1.serializer.news import NewsSerializer, IndexSerializer
from app1.extensions.filter import SelfFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, filters
from app1.extensions.auth import UserAnonTokenAuthentication
from app1.extensions.throttle import NewsCreateRateThrottle


class NewsFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = News
        fields = ["latest_id", ]


class NewsView(DigListModelMixin, DigCreateModelMixin, GenericViewSet, DigDestroyModelMixin, DigUpdateModelMixin):
    filter_backends = [SelfFilterBackend, DjangoFilterBackend]
    filterset_class = NewsFilterSet

    # 未删除 & 属于当前用户创建的新闻资讯
    queryset = News.objects.filter(deleted=False).order_by('-id')
    serializer_class = NewsSerializer

    # 自定义的类变量
    throttle_objects = [NewsCreateRateThrottle(), ]

    def perform_create(self, serializer):
        # 1.创建新闻资讯
        # 2.自己对自己的内容做推荐
        #       - 推荐数量+1
        #       - 推荐记录  用户&资讯
        serializer.save(user=self.request.user)

        # 数据库中已增加成功，调用限流的那个done方法
        for throttle in self.get_throttles():
            throttle.done()

    def get_throttles(self):
        if self.request.method == "POST":
            return self.throttle_objects
        return []


class IndexFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = News
        fields = ["latest_id", 'zone']
        # ?zone=1
        # ?latest_id=99&limit=10


class IndexView(DigListModelMixin, GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = IndexFilterSet

    authentication_classes = [UserAnonTokenAuthentication, ]

    # queryset = models.News.objects.filter(deleted=False, status=2).order_by('-id')
    queryset = News.objects.filter(deleted=False).order_by('-id')
    serializer_class = IndexSerializer
