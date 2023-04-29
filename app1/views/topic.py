from app1.extensions.mixins import DigCreateModelMixin, DigDestroyModelMixin, DigUpdateModelMixin, DigListModelMixin
from app1.serializer.topic import TopicSerializer
from app1.models import Topic
from rest_framework.viewsets import GenericViewSet
from app1.extensions.filter import SelfFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, filters


class TopicFilterSet(FilterSet):
    # ?latest_id=99             ->  id<99
    # ?latest_id=99&limit=10    ->  id<99  limit 10
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = Topic
        fields = ["latest_id", ]


class TopicView(GenericViewSet, DigCreateModelMixin, DigDestroyModelMixin, DigListModelMixin, DigUpdateModelMixin):
    filter_backends = [SelfFilterBackend, DjangoFilterBackend]
    filterset_class = TopicFilterSet
    serializer_class = TopicSerializer
    queryset = Topic.objects.filter(deleted=False).order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
