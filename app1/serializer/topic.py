from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import app1.models as models


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ['id', "title", "is_hot"]
        # read_only_fields = ['is_hot']
        extra_kwargs = {'is_hot': {'read_only': True}, }
