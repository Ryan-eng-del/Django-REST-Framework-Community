from rest_framework import serializers
import app1.models as models
from rest_framework.exceptions import ValidationError


class NewsSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField(read_only=True)
    topic_title = serializers.CharField(
        source="topic.title", read_only=True)
    zone_title = serializers.CharField(
        source="get_zone_display", read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = models.News
        fields = ['id', "title", "url",
                  'image', 'topic_id', "zone",
                  "zone_title", 'image_list', "topic_title", 'collect_count', 'recommend_count', 'comment_count',
                  "status"]

        read_only_fields = ['collect_count',
                            'recommend_count', 'comment_count']

        extra_kwargs = {
            'topic_id': {'write_only': True},  # 新增时，topic=1
            'image': {'write_only': True},  # 图片地址   xxxx,xxxx,xxxx
            'zone': {'write_only': True},
        }

    def get_image_list(self, obj):
        if not obj.image:
            return []
        return obj.image.split(',')

    def validate_topic(self, value):
        if not value:
            return value
        request = self.context['request']
        exists = models.Topic.objects.filter(
            deleted=False, id=value.id, user=request.user).exists()
        if not exists:
            raise ValidationError("话题不存在")
        return value

    def validate_title(self, value):
        url = self.initial_data.get('url')
        image = self.initial_data.get('image')
        zone = self.initial_data.get('zone')

        if url and image:
            raise ValidationError("请求数据错误")
        if not url and not image:
            if zone == 3:
                raise ValidationError("分区选择错误")
        return value

    def create(self, validated_data):

        request = self.context["request"]

        # 1.创建新闻资讯
        new_object = models.News.objects.create(
            recommend_count=1, **validated_data)

        # 2.推荐记录
        models.Recommend.objects.create(
            news=new_object,
            user=request.user
        )

        return new_object


class IndexSubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ['id', 'title', 'is_hot']


class IndexSubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ['id', 'username', ]


class IndexSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField()
    # 调用了 get_collect 方法
    collect = serializers.SerializerMethodField()
    recommend = serializers.SerializerMethodField()

    zone = serializers.CharField(source='get_zone_display')
    topic = IndexSubTopicSerializer(read_only=True)
    user = IndexSubUserSerializer(read_only=True)

    class Meta:
        model = models.News
        fields = ['id', "title", "url", 'image_list', 'topic', "zone", "user", 'collect',
                  'recommend', 'comment_count', ]

    def get_image_list(self, obj):
        if not obj.image:
            return []
        return obj.image.split(',')

    def get_collect(self, obj):
        request = self.context['request']
        if not request.user:
            return {'count': obj.collect_count, 'has_collect': False}

        exists = models.Collect.objects.filter(
            user=request.user, news=obj).exists()
        return {'count': obj.collect_count, 'has_collect': exists}

    def get_recommend(self, obj):
        request = self.context['request']
        if not request.user:
            return {'count': obj.recommend_count, 'has_recommend': False}
        exists = models.Recommend.objects.filter(
            user=request.user, news=obj).exists()
        return {'count': obj.recommend_count, 'has_recommend': exists}
