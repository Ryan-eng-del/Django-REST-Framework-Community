from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from django_filters import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

from app1 import models
from app1.serializer.recommend import RecommendSerializer
from app1.extensions.filter import SelfFilterBackend
from app1.extensions.mixins import DigCreateModelMixin, DigListModelMixin
from app1.extensions import return_code


class RecommendFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = models.Recommend
        fields = ["latest_id", ]


class RecommendView(DigCreateModelMixin, DigListModelMixin, GenericViewSet):
    """ 推荐接口 """
    filter_backends = [SelfFilterBackend, DjangoFilterBackend]
    filterset_class = RecommendFilterSet

    queryset = models.Recommend.objects
    serializer_class = RecommendSerializer

    def perform_create(self, serializer):
        user = self.request.user
        instance = models.Recommend.objects.filter(
            user=user, **serializer.validated_data).first()
        if not instance:
            instance = serializer.save(user=user)
            instance.news.recommend_count += 1
            instance.news.save()
            return Response({"code": return_code.SUCCESS, 'data': {'active': True}})
        else:
            instance.delete()
            instance.news.recommend_count -= 1
            instance.news.save()
            return Response({"code": return_code.SUCCESS, 'data': {'active': False}})
