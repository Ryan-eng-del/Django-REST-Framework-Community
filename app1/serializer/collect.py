from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app1 import models


class CollectSubNewsSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.News
        fields = ['id', 'title', 'url', "image_list"]

    def get_image_list(self, obj):
        if not obj.image:
            return []

        return obj.image.split(',')


class CollectSerializer(serializers.ModelSerializer):
    news_info = CollectSubNewsSerializer(read_only=True, source="news")

    # news=2
    class Meta:
        model = models.Collect
        fields = ['id', "news", "news_info"]
        extra_kwargs = {'news': {'write_only': True}}

    def validate_news(self, value):
        if value.deleted:
            raise ValidationError("资讯不存在")
        return value
