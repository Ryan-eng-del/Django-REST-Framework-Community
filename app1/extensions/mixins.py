from rest_framework import mixins
from rest_framework.response import Response
from app1.extensions import return_code


class DigCreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        # get_serializer 找我们的视图类定义的 Serializer 类并实例化类
        serializer = self.get_serializer(data=request.data)
        # 1. 异常处理a  Serializer 数据校验
        if not serializer.is_valid():
            return Response({"code": return_code.VALIDATE_ERROR, 'detail': serializer.errors})
        # 2. 优化perform_create
        res = self.perform_create(serializer)
        # 3. 返回数据的处理 Serializer 序列化
        return res or Response({"code": return_code.SUCCESS, 'data': serializer.data})


class DigDestroyModelMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        res = self.perform_destroy(instance)
        return res or Response({"code": return_code.SUCCESS})


class DigListModelMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({"code": return_code.SUCCESS, 'data': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({"code": return_code.SUCCESS, 'data': serializer.data})


class DigUpdateModelMixin(mixins.UpdateModelMixin):
    def destroy(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({"code": return_code.VALIDATE_ERROR, 'detail': serializer.errors})
        res = self.perform_update(serializer)
        return res or Response({"code": return_code.SUCCESS, 'data': serializer.data})
