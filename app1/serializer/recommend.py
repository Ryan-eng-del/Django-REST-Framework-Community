from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app1 import models


class RecommendSubNewsSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.News
        fields = ['id', 'title', 'url', "image_list"]

    def get_image_list(self, obj):
        if not obj.image:
            return []
        return obj.image.split(',')


class RecommendSerializer(serializers.ModelSerializer):
    news_info = RecommendSubNewsSerializer(read_only=True, source="news")

    class Meta:
        model = models.Recommend
        fields = ['id', "news", "news_info"]
        extra_kwargs = {'news': {'write_only': True}}
