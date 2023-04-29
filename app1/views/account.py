import uuid
import datetime
from rest_framework.viewsets import GenericViewSet
from app1.extensions.mixins import DigCreateModelMixin
from app1.serializer import account
from rest_framework.views import APIView
from rest_framework.response import Response
from app1.extensions import return_code
from app1 import models
from django.db.models import Q


# 用户注册
class RegisterView(GenericViewSet, DigCreateModelMixin):
    authentication_classes = []
    permission_classes = []
    serializer_class = account.RegisterSerializer

    def perform_create(self, serializer):
        serializer.validated_data.pop("confirm_password")
        serializer.save()


# 用户登录
class AuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = account.AuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"code": return_code.AUTH_FAILED, 'detail': serializer.errors})

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        phone = serializer.validated_data.get("phone")

        user_object = models.UserInfo.objects.filter(
            Q(Q(username=username) | Q(phone=phone)), password=password).first()

        if not user_object:
            return Response({"code": return_code.VALIDATE_ERROR, "error": "用户名或密码错误"})

        token = str(uuid.uuid4())
        user_object.token = token

        # 设置token有效期：当前时间 + 2周
        user_object.token_expires = datetime.datetime.now() + datetime.timedelta(weeks=2)
        user_object.save()

        return Response({"code": return_code.SUCCESS, "data": {"token": token, "name": user_object.username}})
